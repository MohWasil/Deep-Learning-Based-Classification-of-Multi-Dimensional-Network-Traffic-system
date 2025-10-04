import gradio as gr
import requests
import pandas as pd
import traceback

UBUNTU_API = "http://192.168.0.104:8000/latest"
AUTO_REFRESH_SECONDS = 5  # interval for automatic refresh

def fetch(limit=50):
    try:
        r = requests.get(f"{UBUNTU_API}?limit={limit}", timeout=3)
        data = r.json().get("flows", [])
        # ensure consistent columns even if empty
        df = pd.DataFrame(data)
        expected_cols = ["timestamp","src_ip","dst_ip","decision","binary_score","attack_label","app_label"]
        for c in expected_cols:
            if c not in df.columns:
                df[c] = None
        # reorder columns
        df = df[expected_cols]
        return df
    except Exception as e:
        # return a single-row DataFrame with the error so Gradio displays it
        return pd.DataFrame({
            "timestamp": [None],
            "src_ip": [None],
            "dst_ip": [None],
            "decision": [None],
            "binary_score": [None],
            "attack_label": [None],
            "app_label": [f"ERROR: {str(e)}"]
        })

with gr.Blocks() as demo:
    gr.Markdown("## SDN-ML Flow Monitor")
    # Put an explicit elem_id on the refresh button so JS finds it reliably
    refresh = gr.Button("Refresh", elem_id="refresh_btn")
    limit = gr.Slider(10, 200, value=50, step=10, label="Rows to fetch")
    table = gr.Dataframe(
        headers=["timestamp","src_ip","dst_ip","decision","binary_score","attack_label","app_label"],
        datatype=["str","str","str","str","number","str","str"],
        interactive=False,
        row_count=(1, 200)
    )

    def update_table(n):
        try:
            return fetch(n)
        except Exception as e:
            # fallback safe DataFrame
            return pd.DataFrame({
                "timestamp": [None],
                "src_ip": [None],
                "dst_ip": [None],
                "decision": [None],
                "binary_score": [None],
                "attack_label": [None],
                "app_label": [f"ERROR: {traceback.format_exc()}"]
            })

    # Manual refresh
    refresh.click(fn=update_table, inputs=limit, outputs=table)

    # Also load initially (safe: many Gradio versions support .load without 'every')
    try:
        demo.load(fn=update_table, inputs=limit, outputs=table)
    except Exception:
        # if .load(...) with no every fails on your version, ignore — manual refresh + JS will handle updates
        pass

    # Auto-refresh via a tiny client-side script that clicks the Refresh button every N seconds.
    # This approach works across Gradio versions because it uses the DOM to emulate a user click.
    # We place the script in an HTML component so it runs in the browser when the interface loads.
    auto_js = f"""
    <script>
    (function() {{
        function clickRefresh() {{
            // 'refresh_btn' is the elem_id we set above
            var wrapper = document.getElementById('refresh_btn');
            if (!wrapper) return;
            // The actual HTML button is usually inside the wrapper; find it
            var btn = wrapper.querySelector('button');
            if (!btn) return;
            // Only click if button is enabled
            if (!btn.disabled) {{
                btn.click();
            }}
        }}
        // Start after a short delay so initial load can complete
        setTimeout(function() {{
            clickRefresh(); // initial call
            setInterval(clickRefresh, {int(AUTO_REFRESH_SECONDS * 1000)});
        }}, 1000);
    }})();
    </script>
    """
    gr.HTML(auto_js)
    
demo.launch(server_name="0.0.0.0", server_port=7860)
