import os
import time

import obsws_python as obs


def main():
    host = os.getenv("OBSWS_HOST", "localhost")
    port = int(os.getenv("OBSWS_PORT", 4455))
    password = os.getenv("OBSWS_PASSWORD", "")

    with obs.ReqClient(host=host, port=port, password=password) as client:
        resp = client.get_scene_list()
        scenes = [di.get("sceneName") for di in reversed(resp.scenes)]

        for scene in scenes:
            print(f"Switching to scene {scene}")
            client.set_current_program_scene(scene_name=scene)
            time.sleep(0.5)


if __name__ == "__main__":
    main()
