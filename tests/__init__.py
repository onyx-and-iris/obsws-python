import os

import obsws_python as obs

req_cl = obs.ReqClient(
    host=os.getenv("OBSWS_TEST_HOST", "localhost"),
    port=int(os.getenv("OBSWS_TEST_PORT", 4455)),
    password=os.getenv("OBSWS_TEST_PASSWORD", ""),
)


def setup_module():
    req_cl.create_scene(scene_name="START_TEST")
    req_cl.create_scene(scene_name="BRB_TEST")
    req_cl.create_scene(scene_name="END_TEST")


def teardown_module():
    req_cl.remove_scene(scene_name="START_TEST")
    req_cl.remove_scene(scene_name="BRB_TEST")
    req_cl.remove_scene(scene_name="END_TEST")
    resp = req_cl.get_studio_mode_enabled()
    if resp.studio_mode_enabled:
        req_cl.set_studio_mode_enabled(studio_mode_enabled=False)
    req_cl.base_client.ws.close()
