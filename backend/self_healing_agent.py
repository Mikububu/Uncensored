import json
import os
import time
from datetime import datetime

CONFIG_PATH = "config/model_overrides.json"

class SelfHealingAgent:
    def __init__(self):
        self.config_path = CONFIG_PATH
        self._ensure_config()

    def _ensure_config(self):
        """Ensure the overrides file exists."""
        if not os.path.exists("config"):
            os.makedirs("config")
        
        if not os.path.exists(self.config_path):
            with open(self.config_path, 'w') as f:
                json.dump({}, f)

    def load_config(self):
        """Load current overrides."""
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except:
            return {}

    def report_failure(self, model_id, error_msg):
        """Analyze failure and apply fix if needed."""
        print(f"🚑 HEALER: Analyzing failure for {model_id}: {error_msg}")
        
        overrides = self.load_config()
        current_settings = overrides.get(model_id, {})
        
        # Detection Logic
        if "CUDA out of memory" in error_msg or "OOM" in error_msg:
            print(f"🚑 DIAGNOSIS: {model_id} IS OOM.")
            self._apply_downgrade(model_id, current_settings, "resolution")
            
        elif "Timeout" in error_msg or "timed out" in error_msg:
             print(f"🚑 DIAGNOSIS: {model_id} TIMED OUT.")
             # Timeout might mean model is too heavy or steps too high
             self._apply_downgrade(model_id, current_settings, "steps")
             
        elif "No image data" in error_msg:
             print(f"🚑 DIAGNOSIS: {model_id} CRASHED (Empty Result).")
             # Likely VRAM issue or missing file. Try resolution downgrade first.
             self._apply_downgrade(model_id, current_settings, "resolution")

    def _apply_downgrade(self, model_id, settings, type):
        """Apply the specific downgrade strategy."""
        overrides = self.load_config()
        new_settings = overrides.get(model_id, {})
        
        if type == "resolution":
            current_w = new_settings.get("width", 1024)
            current_h = new_settings.get("height", 1024)
            
            if current_w > 768:
                new_settings["width"] = 768
                new_settings["height"] = 1024 # Portrait safe
                print(f"🩹 FIX APPLIED: Downgraded {model_id} to 768px width.")
            elif current_w > 512:
                new_settings["width"] = 512
                new_settings["height"] = 768
                print(f"🩹 FIX APPLIED: Downgraded {model_id} to 512px width (Safety Mode).")
            else:
                 print(f"⚠️ WARNING: {model_id} is already at min spec. Cannot heal further.")
        
        elif type == "steps":
             # Cap steps
             new_settings["max_steps"] = 20
             print(f"🩹 FIX APPLIED: Capped {model_id} to 20 steps.")

        overrides[model_id] = new_settings
        
        # Save
        with open(self.config_path, 'w') as f:
            json.dump(overrides, f, indent=2)
            
    def get_overrides(self, model_id):
        """Get overrides for a specific model."""
        cfg = self.load_config()
        return cfg.get(model_id, {})
