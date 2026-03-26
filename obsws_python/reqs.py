import logging
from collections.abc import Mapping
from typing import Any, Optional
from warnings import warn

from .baseclient import ObsClient
from .error import OBSSDKError, OBSSDKRequestError
from .util import as_dataclass

"""
A class to interact with obs-websocket requests
defined in official github repo
https://github.com/obsproject/obs-websocket/blob/master/docs/generated/protocol.md#Requests
"""

logger = logging.getLogger(__name__)


class ReqClient:
    def __init__(self, **kwargs):
        self.logger = logger.getChild(self.__class__.__name__)
        self.base_client = ObsClient(**kwargs)
        try:
            success = self.base_client.authenticate()
            self.logger.info(
                f"Successfully identified {self} with the server using RPC version:{success['negotiatedRpcVersion']}"
            )
        except OBSSDKError as e:
            self.logger.error(f"{type(e).__name__}: {e}")
            raise

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.disconnect()

    def __repr__(self):
        return type(
            self
        ).__name__ + "(host='{host}', port={port}, password='{password}', timeout={timeout})".format(
            **self.base_client.__dict__,
        )

    def __str__(self):
        return type(self).__name__

    def disconnect(self):
        self.base_client.ws.close()

    def send(self, param, data=None, raw=False):
        try:
            response = self.base_client.req(param, data)
            if not response["requestStatus"]["result"]:
                raise OBSSDKRequestError(
                    response["requestType"],
                    response["requestStatus"]["code"],
                    response["requestStatus"].get("comment"),
                )
        except OBSSDKRequestError as e:
            self.logger.exception(f"{type(e).__name__}: {e}")
            raise
        if "responseData" in response:
            if raw:
                return response["responseData"]
            return as_dataclass(response["requestType"], response["responseData"])

    # === AUTO-GENERATED METHODS BELOW ===
    def get_canvas_list(self):
        """
        Gets an array of canvases in OBS.


        """
        payload = {}
        return self.send("GetCanvasList", payload)

    def get_persistent_data(self, *, realm: str, slot_name: str):
        """
        Gets the value of a "slot" from the selected persistent data realm.

            :param realm: The data realm to select. `OBS_WEBSOCKET_DATA_REALM_GLOBAL` or `OBS_WEBSOCKET_DATA_REALM_PROFILE`
            :type realm: str
            :param slot_name: The name of the slot to retrieve data from
            :type slot_name: str
        """
        payload = {
            "realm": realm,
            "slotName": slot_name,
        }
        return self.send("GetPersistentData", payload)

    def set_persistent_data(self, *, realm: str, slot_name: str, slot_value: Any):
        """
        Sets the value of a "slot" from the selected persistent data realm.

            :param realm: The data realm to select. `OBS_WEBSOCKET_DATA_REALM_GLOBAL` or `OBS_WEBSOCKET_DATA_REALM_PROFILE`
            :type realm: str
            :param slot_name: The name of the slot to retrieve data from
            :type slot_name: str
            :param slot_value: The value to apply to the slot
            :type slot_value: Any
        """
        payload = {
            "realm": realm,
            "slotName": slot_name,
            "slotValue": slot_value,
        }
        return self.send("SetPersistentData", payload)

    def get_scene_collection_list(self):
        """
        Gets an array of all scene collections


        """
        payload = {}
        return self.send("GetSceneCollectionList", payload)

    def set_current_scene_collection(self, *, scene_collection_name: str):
        """
            Switches to a scene collection.

        Note: This will block until the collection has finished changing.

                :param scene_collection_name: Name of the scene collection to switch to
                :type scene_collection_name: str
        """
        payload = {
            "sceneCollectionName": scene_collection_name,
        }
        return self.send("SetCurrentSceneCollection", payload)

    def create_scene_collection(self, *, scene_collection_name: str):
        """
            Creates a new scene collection, switching to it in the process.

        Note: This will block until the collection has finished changing.

                :param scene_collection_name: Name for the new scene collection
                :type scene_collection_name: str
        """
        payload = {
            "sceneCollectionName": scene_collection_name,
        }
        return self.send("CreateSceneCollection", payload)

    def get_profile_list(self):
        """
        Gets an array of all profiles


        """
        payload = {}
        return self.send("GetProfileList", payload)

    def set_current_profile(self, *, profile_name: str):
        """
        Switches to a profile.

            :param profile_name: Name of the profile to switch to
            :type profile_name: str
        """
        payload = {
            "profileName": profile_name,
        }
        return self.send("SetCurrentProfile", payload)

    def create_profile(self, *, profile_name: str):
        """
        Creates a new profile, switching to it in the process

            :param profile_name: Name for the new profile
            :type profile_name: str
        """
        payload = {
            "profileName": profile_name,
        }
        return self.send("CreateProfile", payload)

    def remove_profile(self, *, profile_name: str):
        """
        Removes a profile. If the current profile is chosen, it will change to a different profile first.

            :param profile_name: Name of the profile to remove
            :type profile_name: str
        """
        payload = {
            "profileName": profile_name,
        }
        return self.send("RemoveProfile", payload)

    def get_profile_parameter(self, *, parameter_category: str, parameter_name: str):
        """
        Gets a parameter from the current profile's configuration.

            :param parameter_category: Category of the parameter to get
            :type parameter_category: str
            :param parameter_name: Name of the parameter to get
            :type parameter_name: str
        """
        payload = {
            "parameterCategory": parameter_category,
            "parameterName": parameter_name,
        }
        return self.send("GetProfileParameter", payload)

    def set_profile_parameter(
        self, *, parameter_category: str, parameter_name: str, parameter_value: str
    ):
        """
        Sets the value of a parameter in the current profile's configuration.

            :param parameter_category: Category of the parameter to set
            :type parameter_category: str
            :param parameter_name: Name of the parameter to set
            :type parameter_name: str
            :param parameter_value: Value of the parameter to set. Use `null` to delete
            :type parameter_value: str
        """
        payload = {
            "parameterCategory": parameter_category,
            "parameterName": parameter_name,
            "parameterValue": parameter_value,
        }
        return self.send("SetProfileParameter", payload)

    def get_video_settings(self):
        """
            Gets the current video settings.

        Note: To get the true FPS value, divide the FPS numerator by the FPS denominator. Example: `60000/1001`


        """
        payload = {}
        return self.send("GetVideoSettings", payload)

    def set_video_settings(
        self,
        *,
        fps_numerator: Optional[int] = None,
        fps_denominator: Optional[int] = None,
        base_width: Optional[int] = None,
        base_height: Optional[int] = None,
        output_width: Optional[int] = None,
        output_height: Optional[int] = None,
    ):
        """
            Sets the current video settings.

        Note: Fields must be specified in pairs. For example, you cannot set only `baseWidth` without needing to specify `baseHeight`.

                :param fps_numerator: Numerator of the fractional FPS value
                :type fps_numerator: int, optional
                :param fps_denominator: Denominator of the fractional FPS value
                :type fps_denominator: int, optional
                :param base_width: Width of the base (canvas) resolution in pixels
                :type base_width: int, optional
                :param base_height: Height of the base (canvas) resolution in pixels
                :type base_height: int, optional
                :param output_width: Width of the output resolution in pixels
                :type output_width: int, optional
                :param output_height: Height of the output resolution in pixels
                :type output_height: int, optional
        """
        payload = {
            "fpsNumerator": fps_numerator,
            "fpsDenominator": fps_denominator,
            "baseWidth": base_width,
            "baseHeight": base_height,
            "outputWidth": output_width,
            "outputHeight": output_height,
        }
        return self.send("SetVideoSettings", payload)

    def get_stream_service_settings(self):
        """
        Gets the current stream service settings (stream destination).


        """
        payload = {}
        return self.send("GetStreamServiceSettings", payload)

    def set_stream_service_settings(
        self, *, stream_service_type: str, stream_service_settings: Mapping
    ):
        """
            Sets the current stream service settings (stream destination).

        Note: Simple RTMP settings can be set with type `rtmp_custom` and the settings fields `server` and `key`.

                :param stream_service_type: Type of stream service to apply. Example: `rtmp_common` or `rtmp_custom`
                :type stream_service_type: str
                :param stream_service_settings: Settings to apply to the service
                :type stream_service_settings: Mapping
        """
        payload = {
            "streamServiceType": stream_service_type,
            "streamServiceSettings": stream_service_settings,
        }
        return self.send("SetStreamServiceSettings", payload)

    def get_record_directory(self):
        """
        Gets the current directory that the record output is set to.


        """
        payload = {}
        return self.send("GetRecordDirectory", payload)

    def set_record_directory(self, *, record_directory: str):
        """
        Sets the current directory that the record output writes files to.

            :param record_directory: Output directory
            :type record_directory: str
        """
        payload = {
            "recordDirectory": record_directory,
        }
        return self.send("SetRecordDirectory", payload)

    def get_source_filter_kind_list(self):
        """
            Gets an array of all available source filter kinds.

        Similar to `GetInputKindList`


        """
        payload = {}
        return self.send("GetSourceFilterKindList", payload)

    def get_source_filter_list(
        self,
        *,
        canvas_uuid: Optional[str] = None,
        source_name: Optional[str] = None,
        source_uuid: Optional[str] = None,
    ):
        """
        Gets an array of all of a source's filters.

            :param canvas_uuid: UUID of the canvas the source is in, if using the sourceName field
            :type canvas_uuid: str, optional
            :param source_name: Name of the source
            :type source_name: str, optional
            :param source_uuid: UUID of the source
            :type source_uuid: str, optional
        """
        payload = {
            "canvasUuid": canvas_uuid,
            "sourceName": source_name,
            "sourceUuid": source_uuid,
        }
        return self.send("GetSourceFilterList", payload)

    def get_source_filter_default_settings(self, *, filter_kind: str):
        """
        Gets the default settings for a filter kind.

            :param filter_kind: Filter kind to get the default settings for
            :type filter_kind: str
        """
        payload = {
            "filterKind": filter_kind,
        }
        return self.send("GetSourceFilterDefaultSettings", payload)

    def create_source_filter(
        self,
        *,
        canvas_uuid: Optional[str] = None,
        source_name: Optional[str] = None,
        source_uuid: Optional[str] = None,
        filter_name: str,
        filter_kind: str,
        filter_settings: Optional[Mapping] = None,
    ):
        """
        Creates a new filter, adding it to the specified source.

            :param canvas_uuid: UUID of the canvas the source is in, if using the sourceName field
            :type canvas_uuid: str, optional
            :param source_name: Name of the source to add the filter to
            :type source_name: str, optional
            :param source_uuid: UUID of the source to add the filter to
            :type source_uuid: str, optional
            :param filter_name: Name of the new filter to be created
            :type filter_name: str
            :param filter_kind: The kind of filter to be created
            :type filter_kind: str
            :param filter_settings: Settings object to initialize the filter with
            :type filter_settings: Mapping, optional
        """
        payload = {
            "canvasUuid": canvas_uuid,
            "sourceName": source_name,
            "sourceUuid": source_uuid,
            "filterName": filter_name,
            "filterKind": filter_kind,
            "filterSettings": filter_settings,
        }
        return self.send("CreateSourceFilter", payload)

    def remove_source_filter(
        self,
        *,
        canvas_uuid: Optional[str] = None,
        source_name: Optional[str] = None,
        source_uuid: Optional[str] = None,
        filter_name: str,
    ):
        """
        Removes a filter from a source.

            :param canvas_uuid: UUID of the canvas the source is in, if using the sourceName field
            :type canvas_uuid: str, optional
            :param source_name: Name of the source the filter is on
            :type source_name: str, optional
            :param source_uuid: UUID of the source the filter is on
            :type source_uuid: str, optional
            :param filter_name: Name of the filter to remove
            :type filter_name: str
        """
        payload = {
            "canvasUuid": canvas_uuid,
            "sourceName": source_name,
            "sourceUuid": source_uuid,
            "filterName": filter_name,
        }
        return self.send("RemoveSourceFilter", payload)

    def set_source_filter_name(
        self,
        *,
        canvas_uuid: Optional[str] = None,
        source_name: Optional[str] = None,
        source_uuid: Optional[str] = None,
        filter_name: str,
        new_filter_name: str,
    ):
        """
        Sets the name of a source filter (rename).

            :param canvas_uuid: UUID of the canvas the source is in, if using the sourceName field
            :type canvas_uuid: str, optional
            :param source_name: Name of the source the filter is on
            :type source_name: str, optional
            :param source_uuid: UUID of the source the filter is on
            :type source_uuid: str, optional
            :param filter_name: Current name of the filter
            :type filter_name: str
            :param new_filter_name: New name for the filter
            :type new_filter_name: str
        """
        payload = {
            "canvasUuid": canvas_uuid,
            "sourceName": source_name,
            "sourceUuid": source_uuid,
            "filterName": filter_name,
            "newFilterName": new_filter_name,
        }
        return self.send("SetSourceFilterName", payload)

    def get_source_filter(
        self,
        *,
        canvas_uuid: Optional[str] = None,
        source_name: Optional[str] = None,
        source_uuid: Optional[str] = None,
        filter_name: str,
    ):
        """
        Gets the info for a specific source filter.

            :param canvas_uuid: UUID of the canvas the source is in, if using the sourceName field
            :type canvas_uuid: str, optional
            :param source_name: Name of the source
            :type source_name: str, optional
            :param source_uuid: UUID of the source
            :type source_uuid: str, optional
            :param filter_name: Name of the filter
            :type filter_name: str
        """
        payload = {
            "canvasUuid": canvas_uuid,
            "sourceName": source_name,
            "sourceUuid": source_uuid,
            "filterName": filter_name,
        }
        return self.send("GetSourceFilter", payload)

    def set_source_filter_index(
        self,
        *,
        canvas_uuid: Optional[str] = None,
        source_name: Optional[str] = None,
        source_uuid: Optional[str] = None,
        filter_name: str,
        filter_index: int,
    ):
        """
        Sets the index position of a filter on a source.

            :param canvas_uuid: UUID of the canvas the source is in, if using the sourceName field
            :type canvas_uuid: str, optional
            :param source_name: Name of the source the filter is on
            :type source_name: str, optional
            :param source_uuid: UUID of the source the filter is on
            :type source_uuid: str, optional
            :param filter_name: Name of the filter
            :type filter_name: str
            :param filter_index: New index position of the filter
            :type filter_index: int
        """
        payload = {
            "canvasUuid": canvas_uuid,
            "sourceName": source_name,
            "sourceUuid": source_uuid,
            "filterName": filter_name,
            "filterIndex": filter_index,
        }
        return self.send("SetSourceFilterIndex", payload)

    def set_source_filter_settings(
        self,
        *,
        canvas_uuid: Optional[str] = None,
        source_name: Optional[str] = None,
        source_uuid: Optional[str] = None,
        filter_name: str,
        filter_settings: Mapping,
        overlay: Optional[bool] = True,
    ):
        """
        Sets the settings of a source filter.

            :param canvas_uuid: UUID of the canvas the source is in, if using the sourceName field
            :type canvas_uuid: str, optional
            :param source_name: Name of the source the filter is on
            :type source_name: str, optional
            :param source_uuid: UUID of the source the filter is on
            :type source_uuid: str, optional
            :param filter_name: Name of the filter to set the settings of
            :type filter_name: str
            :param filter_settings: Object of settings to apply
            :type filter_settings: Mapping
            :param overlay: True == apply the settings on top of existing ones, False == reset the input to its defaults, then apply settings.
            :type overlay: bool, optional
        """
        payload = {
            "canvasUuid": canvas_uuid,
            "sourceName": source_name,
            "sourceUuid": source_uuid,
            "filterName": filter_name,
            "filterSettings": filter_settings,
            "overlay": overlay,
        }
        return self.send("SetSourceFilterSettings", payload)

    def set_source_filter_enabled(
        self,
        *,
        canvas_uuid: Optional[str] = None,
        source_name: Optional[str] = None,
        source_uuid: Optional[str] = None,
        filter_name: str,
        filter_enabled: bool,
    ):
        """
        Sets the enable state of a source filter.

            :param canvas_uuid: UUID of the canvas the source is in, if using the sourceName field
            :type canvas_uuid: str, optional
            :param source_name: Name of the source the filter is on
            :type source_name: str, optional
            :param source_uuid: UUID of the source the filter is on
            :type source_uuid: str, optional
            :param filter_name: Name of the filter
            :type filter_name: str
            :param filter_enabled: New enable state of the filter
            :type filter_enabled: bool
        """
        payload = {
            "canvasUuid": canvas_uuid,
            "sourceName": source_name,
            "sourceUuid": source_uuid,
            "filterName": filter_name,
            "filterEnabled": filter_enabled,
        }
        return self.send("SetSourceFilterEnabled", payload)

    def get_version(self):
        """
        Gets data about the current plugin and RPC version.


        """
        payload = {}
        return self.send("GetVersion", payload)

    def get_stats(self):
        """
        Gets statistics about OBS, obs-websocket, and the current session.


        """
        payload = {}
        return self.send("GetStats", payload)

    def broadcast_custom_event(self, *, event_data: Mapping):
        """
        Broadcasts a `CustomEvent` to all WebSocket clients. Receivers are clients which are identified and subscribed.

            :param event_data: Data payload to emit to all receivers
            :type event_data: Mapping
        """
        payload = {
            "eventData": event_data,
        }
        return self.send("BroadcastCustomEvent", payload)

    def call_vendor_request(
        self,
        *,
        vendor_name: str,
        request_type: str,
        request_data: Optional[Mapping] = None,
    ):
        """
            Call a request registered to a vendor.

        A vendor is a unique name registered by a third-party plugin or script, which allows for custom requests and events to be added to obs-websocket.
        If a plugin or script implements vendor requests or events, documentation is expected to be provided with them.

                :param vendor_name: Name of the vendor to use
                :type vendor_name: str
                :param request_type: The request type to call
                :type request_type: str
                :param request_data: Object containing appropriate request data
                :type request_data: Mapping, optional
        """
        payload = {
            "vendorName": vendor_name,
            "requestType": request_type,
            "requestData": request_data,
        }
        return self.send("CallVendorRequest", payload)

    def get_hotkey_list(self):
        """
            Gets an array of all hotkey names in OBS.

        Note: Hotkey functionality in obs-websocket comes as-is, and we do not guarantee support if things are broken. In 9/10 usages of hotkey requests, there exists a better, more reliable method via other requests.


        """
        payload = {}
        return self.send("GetHotkeyList", payload)

    def trigger_hotkey_by_name(
        self, *, hotkey_name: str, context_name: Optional[str] = None
    ):
        """
            Triggers a hotkey using its name. See `GetHotkeyList`.

        Note: Hotkey functionality in obs-websocket comes as-is, and we do not guarantee support if things are broken. In 9/10 usages of hotkey requests, there exists a better, more reliable method via other requests.

                :param hotkey_name: Name of the hotkey to trigger
                :type hotkey_name: str
                :param context_name: Name of context of the hotkey to trigger
                :type context_name: str, optional
        """
        payload = {
            "hotkeyName": hotkey_name,
            "contextName": context_name,
        }
        return self.send("TriggerHotkeyByName", payload)

    def trigger_hotkey_by_key_sequence(
        self,
        *,
        key_id: Optional[str] = None,
        key_modifiers: Optional[Mapping] = None,
        shift: Optional[bool] = None,
        control: Optional[bool] = None,
        alt: Optional[bool] = None,
        command: Optional[bool] = None,
    ):
        """
            Triggers a hotkey using a sequence of keys.

        Note: Hotkey functionality in obs-websocket comes as-is, and we do not guarantee support if things are broken. In 9/10 usages of hotkey requests, there exists a better, more reliable method via other requests.

                :param key_id: The OBS key ID to use. See https://github.com/obsproject/obs-studio/blob/master/libobs/obs-hotkeys.h
                :type key_id: str
                :param key_modifiers: Optional mapping for key modifiers (overrides individual shift/control/alt/command if provided)
                :type key_modifiers: Mapping
                :param shift: Press Shift (used if key_modifiers is not provided)
                :type shift: bool
                :param control: Press CTRL (used if key_modifiers is not provided)
                :type control: bool
                :param alt: Press Alt (used if key_modifiers is not provided)
                :type alt: bool
                :param command: Press Command (used if key_modifiers is not provided)
                :type command: bool
        """
        payload = {
            "keyId": key_id,
            "keyModifiers": (
                key_modifiers
                if key_modifiers is not None
                else {
                    "shift": shift,
                    "control": control,
                    "alt": alt,
                    "command": command,
                }
            ),
        }
        return self.send("TriggerHotkeyByKeySequence", payload)

    def sleep(
        self, *, sleep_millis: Optional[int] = None, sleep_frames: Optional[int] = None
    ):
        """
        Sleeps for a time duration or number of frames. Only available in request batches with types `SERIAL_REALTIME` or `SERIAL_FRAME`.

            :param sleep_millis: Number of milliseconds to sleep for (if `SERIAL_REALTIME` mode)
            :type sleep_millis: int, optional
            :param sleep_frames: Number of frames to sleep for (if `SERIAL_FRAME` mode)
            :type sleep_frames: int, optional
        """
        payload = {
            "sleepMillis": sleep_millis,
            "sleepFrames": sleep_frames,
        }
        return self.send("Sleep", payload)

    def get_input_list(self, *, input_kind: Optional[str] = None):
        """
        Gets an array of all inputs in OBS.

            :param input_kind: Restrict the array to only inputs of the specified kind
            :type input_kind: str, optional
        """
        payload = {
            "inputKind": input_kind,
        }
        return self.send("GetInputList", payload)

    def get_input_kind_list(self, *, unversioned: Optional[bool] = False):
        """
        Gets an array of all available input kinds in OBS.

            :param unversioned: True == Return all kinds as unversioned, False == Return with version suffixes (if available)
            :type unversioned: bool, optional
        """
        payload = {
            "unversioned": unversioned,
        }
        return self.send("GetInputKindList", payload)

    def get_special_inputs(self):
        """
        Gets the names of all special inputs.


        """
        payload = {}
        return self.send("GetSpecialInputs", payload)

    def create_input(
        self,
        *,
        canvas_uuid: Optional[str] = None,
        scene_name: Optional[str] = None,
        scene_uuid: Optional[str] = None,
        input_name: str,
        input_kind: str,
        input_settings: Optional[Mapping] = None,
        scene_item_enabled: Optional[bool] = True,
    ):
        """
        Creates a new input, adding it as a scene item to the specified scene.

            :param canvas_uuid: UUID of the canvas the scene is in, if using the sceneName field
            :type canvas_uuid: str, optional
            :param scene_name: Name of the scene to add the input to as a scene item
            :type scene_name: str, optional
            :param scene_uuid: UUID of the scene to add the input to as a scene item
            :type scene_uuid: str, optional
            :param input_name: Name of the new input to created
            :type input_name: str
            :param input_kind: The kind of input to be created
            :type input_kind: str
            :param input_settings: Settings object to initialize the input with
            :type input_settings: Mapping, optional
            :param scene_item_enabled: Whether to set the created scene item to enabled or disabled
            :type scene_item_enabled: bool, optional
        """
        payload = {
            "canvasUuid": canvas_uuid,
            "sceneName": scene_name,
            "sceneUuid": scene_uuid,
            "inputName": input_name,
            "inputKind": input_kind,
            "inputSettings": input_settings,
            "sceneItemEnabled": scene_item_enabled,
        }
        return self.send("CreateInput", payload)

    def remove_input(
        self, *, input_name: Optional[str] = None, input_uuid: Optional[str] = None
    ):
        """
            Removes an existing input.

        Note: Will immediately remove all associated scene items.

                :param input_name: Name of the input to remove
                :type input_name: str, optional
                :param input_uuid: UUID of the input to remove
                :type input_uuid: str, optional
        """
        payload = {
            "inputName": input_name,
            "inputUuid": input_uuid,
        }
        return self.send("RemoveInput", payload)

    def set_input_name(
        self,
        *,
        input_name: Optional[str] = None,
        input_uuid: Optional[str] = None,
        new_input_name: str,
    ):
        """
        Sets the name of an input (rename).

            :param input_name: Current input name
            :type input_name: str, optional
            :param input_uuid: Current input UUID
            :type input_uuid: str, optional
            :param new_input_name: New name for the input
            :type new_input_name: str
        """
        payload = {
            "inputName": input_name,
            "inputUuid": input_uuid,
            "newInputName": new_input_name,
        }
        return self.send("SetInputName", payload)

    def get_input_default_settings(self, *, input_kind: str):
        """
        Gets the default settings for an input kind.

            :param input_kind: Input kind to get the default settings for
            :type input_kind: str
        """
        payload = {
            "inputKind": input_kind,
        }
        return self.send("GetInputDefaultSettings", payload)

    def get_input_settings(
        self, *, input_name: Optional[str] = None, input_uuid: Optional[str] = None
    ):
        """
            Gets the settings of an input.

        Note: Does not include defaults. To create the entire settings object, overlay `inputSettings` over the `defaultInputSettings` provided by `GetInputDefaultSettings`.

                :param input_name: Name of the input to get the settings of
                :type input_name: str, optional
                :param input_uuid: UUID of the input to get the settings of
                :type input_uuid: str, optional
        """
        payload = {
            "inputName": input_name,
            "inputUuid": input_uuid,
        }
        return self.send("GetInputSettings", payload)

    def set_input_settings(
        self,
        *,
        input_name: Optional[str] = None,
        input_uuid: Optional[str] = None,
        input_settings: Mapping,
        overlay: Optional[bool] = True,
    ):
        """
        Sets the settings of an input.

            :param input_name: Name of the input to set the settings of
            :type input_name: str, optional
            :param input_uuid: UUID of the input to set the settings of
            :type input_uuid: str, optional
            :param input_settings: Object of settings to apply
            :type input_settings: Mapping
            :param overlay: True == apply the settings on top of existing ones, False == reset the input to its defaults, then apply settings.
            :type overlay: bool, optional
        """
        payload = {
            "inputName": input_name,
            "inputUuid": input_uuid,
            "inputSettings": input_settings,
            "overlay": overlay,
        }
        return self.send("SetInputSettings", payload)

    def get_input_mute(
        self, *, input_name: Optional[str] = None, input_uuid: Optional[str] = None
    ):
        """
        Gets the audio mute state of an input.

            :param input_name: Name of input to get the mute state of
            :type input_name: str, optional
            :param input_uuid: UUID of input to get the mute state of
            :type input_uuid: str, optional
        """
        payload = {
            "inputName": input_name,
            "inputUuid": input_uuid,
        }
        return self.send("GetInputMute", payload)

    def set_input_mute(
        self,
        *,
        input_name: Optional[str] = None,
        input_uuid: Optional[str] = None,
        input_muted: bool,
    ):
        """
        Sets the audio mute state of an input.

            :param input_name: Name of the input to set the mute state of
            :type input_name: str, optional
            :param input_uuid: UUID of the input to set the mute state of
            :type input_uuid: str, optional
            :param input_muted: Whether to mute the input or not
            :type input_muted: bool
        """
        payload = {
            "inputName": input_name,
            "inputUuid": input_uuid,
            "inputMuted": input_muted,
        }
        return self.send("SetInputMute", payload)

    def toggle_input_mute(
        self, *, input_name: Optional[str] = None, input_uuid: Optional[str] = None
    ):
        """
        Toggles the audio mute state of an input.

            :param input_name: Name of the input to toggle the mute state of
            :type input_name: str, optional
            :param input_uuid: UUID of the input to toggle the mute state of
            :type input_uuid: str, optional
        """
        payload = {
            "inputName": input_name,
            "inputUuid": input_uuid,
        }
        return self.send("ToggleInputMute", payload)

    def get_input_volume(
        self, *, input_name: Optional[str] = None, input_uuid: Optional[str] = None
    ):
        """
        Gets the current volume setting of an input.

            :param input_name: Name of the input to get the volume of
            :type input_name: str, optional
            :param input_uuid: UUID of the input to get the volume of
            :type input_uuid: str, optional
        """
        payload = {
            "inputName": input_name,
            "inputUuid": input_uuid,
        }
        return self.send("GetInputVolume", payload)

    def set_input_volume(
        self,
        *,
        input_name: Optional[str] = None,
        input_uuid: Optional[str] = None,
        input_volume_mul: Optional[int] = None,
        input_volume_db: Optional[int] = None,
    ):
        """
        Sets the volume setting of an input.

            :param input_name: Name of the input to set the volume of
            :type input_name: str, optional
            :param input_uuid: UUID of the input to set the volume of
            :type input_uuid: str, optional
            :param input_volume_mul: Volume setting in mul
            :type input_volume_mul: int, optional
            :param input_volume_db: Volume setting in dB
            :type input_volume_db: int, optional
        """
        payload = {
            "inputName": input_name,
            "inputUuid": input_uuid,
            "inputVolumeMul": input_volume_mul,
            "inputVolumeDb": input_volume_db,
        }
        return self.send("SetInputVolume", payload)

    def get_input_audio_balance(
        self, *, input_name: Optional[str] = None, input_uuid: Optional[str] = None
    ):
        """
        Gets the audio balance of an input.

            :param input_name: Name of the input to get the audio balance of
            :type input_name: str, optional
            :param input_uuid: UUID of the input to get the audio balance of
            :type input_uuid: str, optional
        """
        payload = {
            "inputName": input_name,
            "inputUuid": input_uuid,
        }
        return self.send("GetInputAudioBalance", payload)

    def set_input_audio_balance(
        self,
        *,
        input_name: Optional[str] = None,
        input_uuid: Optional[str] = None,
        input_audio_balance: int,
    ):
        """
        Sets the audio balance of an input.

            :param input_name: Name of the input to set the audio balance of
            :type input_name: str, optional
            :param input_uuid: UUID of the input to set the audio balance of
            :type input_uuid: str, optional
            :param input_audio_balance: New audio balance value
            :type input_audio_balance: int
        """
        payload = {
            "inputName": input_name,
            "inputUuid": input_uuid,
            "inputAudioBalance": input_audio_balance,
        }
        return self.send("SetInputAudioBalance", payload)

    def get_input_audio_sync_offset(
        self, *, input_name: Optional[str] = None, input_uuid: Optional[str] = None
    ):
        """
            Gets the audio sync offset of an input.

        Note: The audio sync offset can be negative too!

                :param input_name: Name of the input to get the audio sync offset of
                :type input_name: str, optional
                :param input_uuid: UUID of the input to get the audio sync offset of
                :type input_uuid: str, optional
        """
        payload = {
            "inputName": input_name,
            "inputUuid": input_uuid,
        }
        return self.send("GetInputAudioSyncOffset", payload)

    def set_input_audio_sync_offset(
        self,
        *,
        input_name: Optional[str] = None,
        input_uuid: Optional[str] = None,
        input_audio_sync_offset: int,
    ):
        """
        Sets the audio sync offset of an input.

            :param input_name: Name of the input to set the audio sync offset of
            :type input_name: str, optional
            :param input_uuid: UUID of the input to set the audio sync offset of
            :type input_uuid: str, optional
            :param input_audio_sync_offset: New audio sync offset in milliseconds
            :type input_audio_sync_offset: int
        """
        payload = {
            "inputName": input_name,
            "inputUuid": input_uuid,
            "inputAudioSyncOffset": input_audio_sync_offset,
        }
        return self.send("SetInputAudioSyncOffset", payload)

    def get_input_audio_monitor_type(
        self, *, input_name: Optional[str] = None, input_uuid: Optional[str] = None
    ):
        """
            Gets the audio monitor type of an input.

        The available audio monitor types are:

        - `OBS_MONITORING_TYPE_NONE`
        - `OBS_MONITORING_TYPE_MONITOR_ONLY`
        - `OBS_MONITORING_TYPE_MONITOR_AND_OUTPUT`

                :param input_name: Name of the input to get the audio monitor type of
                :type input_name: str, optional
                :param input_uuid: UUID of the input to get the audio monitor type of
                :type input_uuid: str, optional
        """
        payload = {
            "inputName": input_name,
            "inputUuid": input_uuid,
        }
        return self.send("GetInputAudioMonitorType", payload)

    def set_input_audio_monitor_type(
        self,
        *,
        input_name: Optional[str] = None,
        input_uuid: Optional[str] = None,
        monitor_type: str,
    ):
        """
        Sets the audio monitor type of an input.

            :param input_name: Name of the input to set the audio monitor type of
            :type input_name: str, optional
            :param input_uuid: UUID of the input to set the audio monitor type of
            :type input_uuid: str, optional
            :param monitor_type: Audio monitor type
            :type monitor_type: str
        """
        payload = {
            "inputName": input_name,
            "inputUuid": input_uuid,
            "monitorType": monitor_type,
        }
        return self.send("SetInputAudioMonitorType", payload)

    def get_input_audio_tracks(
        self, *, input_name: Optional[str] = None, input_uuid: Optional[str] = None
    ):
        """
        Gets the enable state of all audio tracks of an input.

            :param input_name: Name of the input
            :type input_name: str, optional
            :param input_uuid: UUID of the input
            :type input_uuid: str, optional
        """
        payload = {
            "inputName": input_name,
            "inputUuid": input_uuid,
        }
        return self.send("GetInputAudioTracks", payload)

    def set_input_audio_tracks(
        self,
        *,
        input_name: Optional[str] = None,
        input_uuid: Optional[str] = None,
        input_audio_tracks: Mapping,
    ):
        """
        Sets the enable state of audio tracks of an input.

            :param input_name: Name of the input
            :type input_name: str, optional
            :param input_uuid: UUID of the input
            :type input_uuid: str, optional
            :param input_audio_tracks: Track settings to apply
            :type input_audio_tracks: Mapping
        """
        payload = {
            "inputName": input_name,
            "inputUuid": input_uuid,
            "inputAudioTracks": input_audio_tracks,
        }
        return self.send("SetInputAudioTracks", payload)

    def get_input_deinterlace_mode(
        self, *, input_name: Optional[str] = None, input_uuid: Optional[str] = None
    ):
        """
            Gets the deinterlace mode of an input.

        Deinterlace Modes:

        - `OBS_DEINTERLACE_MODE_DISABLE`
        - `OBS_DEINTERLACE_MODE_DISCARD`
        - `OBS_DEINTERLACE_MODE_RETRO`
        - `OBS_DEINTERLACE_MODE_BLEND`
        - `OBS_DEINTERLACE_MODE_BLEND_2X`
        - `OBS_DEINTERLACE_MODE_LINEAR`
        - `OBS_DEINTERLACE_MODE_LINEAR_2X`
        - `OBS_DEINTERLACE_MODE_YADIF`
        - `OBS_DEINTERLACE_MODE_YADIF_2X`

        Note: Deinterlacing functionality is restricted to async inputs only.

                :param input_name: Name of the input
                :type input_name: str, optional
                :param input_uuid: UUID of the input
                :type input_uuid: str, optional
        """
        payload = {
            "inputName": input_name,
            "inputUuid": input_uuid,
        }
        return self.send("GetInputDeinterlaceMode", payload)

    def set_input_deinterlace_mode(
        self,
        *,
        input_name: Optional[str] = None,
        input_uuid: Optional[str] = None,
        input_deinterlace_mode: str,
    ):
        """
            Sets the deinterlace mode of an input.

        Note: Deinterlacing functionality is restricted to async inputs only.

                :param input_name: Name of the input
                :type input_name: str, optional
                :param input_uuid: UUID of the input
                :type input_uuid: str, optional
                :param input_deinterlace_mode: Deinterlace mode for the input
                :type input_deinterlace_mode: str
        """
        payload = {
            "inputName": input_name,
            "inputUuid": input_uuid,
            "inputDeinterlaceMode": input_deinterlace_mode,
        }
        return self.send("SetInputDeinterlaceMode", payload)

    def get_input_deinterlace_field_order(
        self, *, input_name: Optional[str] = None, input_uuid: Optional[str] = None
    ):
        """
            Gets the deinterlace field order of an input.

        Deinterlace Field Orders:

        - `OBS_DEINTERLACE_FIELD_ORDER_TOP`
        - `OBS_DEINTERLACE_FIELD_ORDER_BOTTOM`

        Note: Deinterlacing functionality is restricted to async inputs only.

                :param input_name: Name of the input
                :type input_name: str, optional
                :param input_uuid: UUID of the input
                :type input_uuid: str, optional
        """
        payload = {
            "inputName": input_name,
            "inputUuid": input_uuid,
        }
        return self.send("GetInputDeinterlaceFieldOrder", payload)

    def set_input_deinterlace_field_order(
        self,
        *,
        input_name: Optional[str] = None,
        input_uuid: Optional[str] = None,
        input_deinterlace_field_order: str,
    ):
        """
            Sets the deinterlace field order of an input.

        Note: Deinterlacing functionality is restricted to async inputs only.

                :param input_name: Name of the input
                :type input_name: str, optional
                :param input_uuid: UUID of the input
                :type input_uuid: str, optional
                :param input_deinterlace_field_order: Deinterlace field order for the input
                :type input_deinterlace_field_order: str
        """
        payload = {
            "inputName": input_name,
            "inputUuid": input_uuid,
            "inputDeinterlaceFieldOrder": input_deinterlace_field_order,
        }
        return self.send("SetInputDeinterlaceFieldOrder", payload)

    def get_input_properties_list_property_items(
        self,
        *,
        input_name: Optional[str] = None,
        input_uuid: Optional[str] = None,
        property_name: str,
    ):
        """
            Gets the items of a list property from an input's properties.

        Note: Use this in cases where an input provides a dynamic, selectable list of items. For example, display capture, where it provides a list of available displays.

                :param input_name: Name of the input
                :type input_name: str, optional
                :param input_uuid: UUID of the input
                :type input_uuid: str, optional
                :param property_name: Name of the list property to get the items of
                :type property_name: str
        """
        payload = {
            "inputName": input_name,
            "inputUuid": input_uuid,
            "propertyName": property_name,
        }
        return self.send("GetInputPropertiesListPropertyItems", payload)

    def press_input_properties_button(
        self,
        *,
        input_name: Optional[str] = None,
        input_uuid: Optional[str] = None,
        property_name: str,
    ):
        """
            Presses a button in the properties of an input.

        Some known `propertyName` values are:

        - `refreshnocache` - Browser source reload button

        Note: Use this in cases where there is a button in the properties of an input that cannot be accessed in any other way. For example, browser sources, where there is a refresh button.

                :param input_name: Name of the input
                :type input_name: str, optional
                :param input_uuid: UUID of the input
                :type input_uuid: str, optional
                :param property_name: Name of the button property to press
                :type property_name: str
        """
        payload = {
            "inputName": input_name,
            "inputUuid": input_uuid,
            "propertyName": property_name,
        }
        return self.send("PressInputPropertiesButton", payload)

    def get_media_input_status(
        self, *, input_name: Optional[str] = None, input_uuid: Optional[str] = None
    ):
        """
            Gets the status of a media input.

        Media States:

        - `OBS_MEDIA_STATE_NONE`
        - `OBS_MEDIA_STATE_PLAYING`
        - `OBS_MEDIA_STATE_OPENING`
        - `OBS_MEDIA_STATE_BUFFERING`
        - `OBS_MEDIA_STATE_PAUSED`
        - `OBS_MEDIA_STATE_STOPPED`
        - `OBS_MEDIA_STATE_ENDED`
        - `OBS_MEDIA_STATE_ERROR`

                :param input_name: Name of the media input
                :type input_name: str, optional
                :param input_uuid: UUID of the media input
                :type input_uuid: str, optional
        """
        payload = {
            "inputName": input_name,
            "inputUuid": input_uuid,
        }
        return self.send("GetMediaInputStatus", payload)

    def set_media_input_cursor(
        self,
        *,
        input_name: Optional[str] = None,
        input_uuid: Optional[str] = None,
        media_cursor: int,
    ):
        """
            Sets the cursor position of a media input.

        This request does not perform bounds checking of the cursor position.

                :param input_name: Name of the media input
                :type input_name: str, optional
                :param input_uuid: UUID of the media input
                :type input_uuid: str, optional
                :param media_cursor: New cursor position to set
                :type media_cursor: int
        """
        payload = {
            "inputName": input_name,
            "inputUuid": input_uuid,
            "mediaCursor": media_cursor,
        }
        return self.send("SetMediaInputCursor", payload)

    def offset_media_input_cursor(
        self,
        *,
        input_name: Optional[str] = None,
        input_uuid: Optional[str] = None,
        media_cursor_offset: int,
    ):
        """
            Offsets the current cursor position of a media input by the specified value.

        This request does not perform bounds checking of the cursor position.

                :param input_name: Name of the media input
                :type input_name: str, optional
                :param input_uuid: UUID of the media input
                :type input_uuid: str, optional
                :param media_cursor_offset: Value to offset the current cursor position by
                :type media_cursor_offset: int
        """
        payload = {
            "inputName": input_name,
            "inputUuid": input_uuid,
            "mediaCursorOffset": media_cursor_offset,
        }
        return self.send("OffsetMediaInputCursor", payload)

    def trigger_media_input_action(
        self,
        *,
        input_name: Optional[str] = None,
        input_uuid: Optional[str] = None,
        media_action: str,
    ):
        """
        Triggers an action on a media input.

            :param input_name: Name of the media input
            :type input_name: str, optional
            :param input_uuid: UUID of the media input
            :type input_uuid: str, optional
            :param media_action: Identifier of the `ObsMediaInputAction` enum
            :type media_action: str
        """
        payload = {
            "inputName": input_name,
            "inputUuid": input_uuid,
            "mediaAction": media_action,
        }
        return self.send("TriggerMediaInputAction", payload)

    def get_virtual_cam_status(self):
        """
        Gets the status of the virtualcam output.


        """
        payload = {}
        return self.send("GetVirtualCamStatus", payload)

    def toggle_virtual_cam(self):
        """
        Toggles the state of the virtualcam output.


        """
        payload = {}
        return self.send("ToggleVirtualCam", payload)

    def start_virtual_cam(self):
        """
        Starts the virtualcam output.


        """
        payload = {}
        return self.send("StartVirtualCam", payload)

    def stop_virtual_cam(self):
        """
        Stops the virtualcam output.


        """
        payload = {}
        return self.send("StopVirtualCam", payload)

    def get_replay_buffer_status(self):
        """
        Gets the status of the replay buffer output.


        """
        payload = {}
        return self.send("GetReplayBufferStatus", payload)

    def toggle_replay_buffer(self):
        """
        Toggles the state of the replay buffer output.


        """
        payload = {}
        return self.send("ToggleReplayBuffer", payload)

    def start_replay_buffer(self):
        """
        Starts the replay buffer output.


        """
        payload = {}
        return self.send("StartReplayBuffer", payload)

    def stop_replay_buffer(self):
        """
        Stops the replay buffer output.


        """
        payload = {}
        return self.send("StopReplayBuffer", payload)

    def save_replay_buffer(self):
        """
        Saves the contents of the replay buffer output.


        """
        payload = {}
        return self.send("SaveReplayBuffer", payload)

    def get_last_replay_buffer_replay(self):
        """
        Gets the filename of the last replay buffer save file.


        """
        payload = {}
        return self.send("GetLastReplayBufferReplay", payload)

    def get_output_list(self):
        """
        Gets the list of available outputs.


        """
        payload = {}
        return self.send("GetOutputList", payload)

    def get_output_status(self, *, output_name: str):
        """
        Gets the status of an output.

            :param output_name: Output name
            :type output_name: str
        """
        payload = {
            "outputName": output_name,
        }
        return self.send("GetOutputStatus", payload)

    def toggle_output(self, *, output_name: str):
        """
        Toggles the status of an output.

            :param output_name: Output name
            :type output_name: str
        """
        payload = {
            "outputName": output_name,
        }
        return self.send("ToggleOutput", payload)

    def start_output(self, *, output_name: str):
        """
        Starts an output.

            :param output_name: Output name
            :type output_name: str
        """
        payload = {
            "outputName": output_name,
        }
        return self.send("StartOutput", payload)

    def stop_output(self, *, output_name: str):
        """
        Stops an output.

            :param output_name: Output name
            :type output_name: str
        """
        payload = {
            "outputName": output_name,
        }
        return self.send("StopOutput", payload)

    def get_output_settings(self, *, output_name: str):
        """
        Gets the settings of an output.

            :param output_name: Output name
            :type output_name: str
        """
        payload = {
            "outputName": output_name,
        }
        return self.send("GetOutputSettings", payload)

    def set_output_settings(self, *, output_name: str, output_settings: Mapping):
        """
        Sets the settings of an output.

            :param output_name: Output name
            :type output_name: str
            :param output_settings: Output settings
            :type output_settings: Mapping
        """
        payload = {
            "outputName": output_name,
            "outputSettings": output_settings,
        }
        return self.send("SetOutputSettings", payload)

    def get_record_status(self):
        """
        Gets the status of the record output.


        """
        payload = {}
        return self.send("GetRecordStatus", payload)

    def toggle_record(self):
        """
        Toggles the status of the record output.


        """
        payload = {}
        return self.send("ToggleRecord", payload)

    def start_record(self):
        """
        Starts the record output.


        """
        payload = {}
        return self.send("StartRecord", payload)

    def stop_record(self):
        """
        Stops the record output.


        """
        payload = {}
        return self.send("StopRecord", payload)

    def toggle_record_pause(self):
        """
        Toggles pause on the record output.


        """
        payload = {}
        return self.send("ToggleRecordPause", payload)

    def pause_record(self):
        """
        Pauses the record output.


        """
        payload = {}
        return self.send("PauseRecord", payload)

    def resume_record(self):
        """
        Resumes the record output.


        """
        payload = {}
        return self.send("ResumeRecord", payload)

    def split_record_file(self):
        """
        Splits the current file being recorded into a new file.


        """
        payload = {}
        return self.send("SplitRecordFile", payload)

    def create_record_chapter(self, *, chapter_name: Optional[str] = None):
        """
            Adds a new chapter marker to the file currently being recorded.

        Note: As of OBS 30.2.0, the only file format supporting this feature is Hybrid MP4.

                :param chapter_name: Name of the new chapter
                :type chapter_name: str, optional
        """
        payload = {
            "chapterName": chapter_name,
        }
        return self.send("CreateRecordChapter", payload)

    def get_scene_item_list(
        self,
        *,
        canvas_uuid: Optional[str] = None,
        scene_name: Optional[str] = None,
        scene_uuid: Optional[str] = None,
    ):
        """
            Gets a list of all scene items in a scene.

        Scenes only

                :param canvas_uuid: UUID of the canvas the scene is in, if using the sceneName field
                :type canvas_uuid: str, optional
                :param scene_name: Name of the scene to get the items of
                :type scene_name: str, optional
                :param scene_uuid: UUID of the scene to get the items of
                :type scene_uuid: str, optional
        """
        payload = {
            "canvasUuid": canvas_uuid,
            "sceneName": scene_name,
            "sceneUuid": scene_uuid,
        }
        return self.send("GetSceneItemList", payload)

    def get_group_scene_item_list(
        self,
        *,
        canvas_uuid: Optional[str] = None,
        scene_name: Optional[str] = None,
        scene_uuid: Optional[str] = None,
    ):
        """
            Basically GetSceneItemList, but for groups.

        Using groups at all in OBS is discouraged, as they are very broken under the hood. Please use nested scenes instead.

        Groups only

                :param canvas_uuid: UUID of the canvas the group is in, if using the sceneName field
                :type canvas_uuid: str, optional
                :param scene_name: Name of the group to get the items of
                :type scene_name: str, optional
                :param scene_uuid: UUID of the group to get the items of
                :type scene_uuid: str, optional
        """
        payload = {
            "canvasUuid": canvas_uuid,
            "sceneName": scene_name,
            "sceneUuid": scene_uuid,
        }
        return self.send("GetGroupSceneItemList", payload)

    def get_scene_item_id(
        self,
        *,
        canvas_uuid: Optional[str] = None,
        scene_name: Optional[str] = None,
        scene_uuid: Optional[str] = None,
        source_name: str,
        search_offset: Optional[int] = None,
    ):
        """
            Searches a scene for a source, and returns its id.

        Scenes and Groups

                :param canvas_uuid: UUID of the canvas the scene or group is in, if using the sceneName field
                :type canvas_uuid: str, optional
                :param scene_name: Name of the scene or group to search in
                :type scene_name: str, optional
                :param scene_uuid: UUID of the scene or group to search in
                :type scene_uuid: str, optional
                :param source_name: Name of the source to find
                :type source_name: str
                :param search_offset: Number of matches to skip during search. >= 0 means first forward. -1 means last (top) item
                :type search_offset: int, optional
        """
        payload = {
            "canvasUuid": canvas_uuid,
            "sceneName": scene_name,
            "sceneUuid": scene_uuid,
            "sourceName": source_name,
            "searchOffset": search_offset,
        }
        return self.send("GetSceneItemId", payload)

    def get_scene_item_source(
        self,
        *,
        canvas_uuid: Optional[str] = None,
        scene_name: Optional[str] = None,
        scene_uuid: Optional[str] = None,
        scene_item_id: int,
    ):
        """
        Gets the source associated with a scene item.

            :param canvas_uuid: UUID of the canvas the scene is in, if using the sceneName field
            :type canvas_uuid: str, optional
            :param scene_name: Name of the scene the item is in
            :type scene_name: str, optional
            :param scene_uuid: UUID of the scene the item is in
            :type scene_uuid: str, optional
            :param scene_item_id: Numeric ID of the scene item
            :type scene_item_id: int
        """
        payload = {
            "canvasUuid": canvas_uuid,
            "sceneName": scene_name,
            "sceneUuid": scene_uuid,
            "sceneItemId": scene_item_id,
        }
        return self.send("GetSceneItemSource", payload)

    def create_scene_item(
        self,
        *,
        canvas_uuid: Optional[str] = None,
        scene_name: Optional[str] = None,
        scene_uuid: Optional[str] = None,
        source_name: Optional[str] = None,
        source_uuid: Optional[str] = None,
        scene_item_enabled: Optional[bool] = True,
    ):
        """
            Creates a new scene item using a source.

        Scenes only

                :param canvas_uuid: UUID of the canvas the scene is in, if using the sceneName field
                :type canvas_uuid: str, optional
                :param scene_name: Name of the scene to create the new item in
                :type scene_name: str, optional
                :param scene_uuid: UUID of the scene to create the new item in
                :type scene_uuid: str, optional
                :param source_name: Name of the source to add to the scene
                :type source_name: str, optional
                :param source_uuid: UUID of the source to add to the scene
                :type source_uuid: str, optional
                :param scene_item_enabled: Enable state to apply to the scene item on creation
                :type scene_item_enabled: bool, optional
        """
        payload = {
            "canvasUuid": canvas_uuid,
            "sceneName": scene_name,
            "sceneUuid": scene_uuid,
            "sourceName": source_name,
            "sourceUuid": source_uuid,
            "sceneItemEnabled": scene_item_enabled,
        }
        return self.send("CreateSceneItem", payload)

    def remove_scene_item(
        self,
        *,
        canvas_uuid: Optional[str] = None,
        scene_name: Optional[str] = None,
        scene_uuid: Optional[str] = None,
        scene_item_id: int,
    ):
        """
            Removes a scene item from a scene.

        Scenes only

                :param canvas_uuid: UUID of the canvas the scene is in, if using the sceneName field
                :type canvas_uuid: str, optional
                :param scene_name: Name of the scene the item is in
                :type scene_name: str, optional
                :param scene_uuid: UUID of the scene the item is in
                :type scene_uuid: str, optional
                :param scene_item_id: Numeric ID of the scene item
                :type scene_item_id: int
        """
        payload = {
            "canvasUuid": canvas_uuid,
            "sceneName": scene_name,
            "sceneUuid": scene_uuid,
            "sceneItemId": scene_item_id,
        }
        return self.send("RemoveSceneItem", payload)

    def duplicate_scene_item(
        self,
        *,
        canvas_uuid: Optional[str] = None,
        scene_name: Optional[str] = None,
        scene_uuid: Optional[str] = None,
        scene_item_id: int,
        destination_scene_name: Optional[str] = None,
        destination_scene_uuid: Optional[str] = None,
    ):
        """
            Duplicates a scene item, copying all transform and crop info.

        Scenes only

                :param canvas_uuid: UUID of the canvas the scene is in, if using the sceneName field
                :type canvas_uuid: str, optional
                :param scene_name: Name of the scene the item is in
                :type scene_name: str, optional
                :param scene_uuid: UUID of the scene the item is in
                :type scene_uuid: str, optional
                :param scene_item_id: Numeric ID of the scene item
                :type scene_item_id: int
                :param destination_scene_name: Name of the scene to create the duplicated item in
                :type destination_scene_name: str, optional
                :param destination_scene_uuid: UUID of the scene to create the duplicated item in
                :type destination_scene_uuid: str, optional
        """
        payload = {
            "canvasUuid": canvas_uuid,
            "sceneName": scene_name,
            "sceneUuid": scene_uuid,
            "sceneItemId": scene_item_id,
            "destinationSceneName": destination_scene_name,
            "destinationSceneUuid": destination_scene_uuid,
        }
        return self.send("DuplicateSceneItem", payload)

    def get_scene_item_transform(
        self,
        *,
        canvas_uuid: Optional[str] = None,
        scene_name: Optional[str] = None,
        scene_uuid: Optional[str] = None,
        scene_item_id: int,
    ):
        """
            Gets the transform and crop info of a scene item.

        Scenes and Groups

                :param canvas_uuid: UUID of the canvas the scene is in, if using the sceneName field
                :type canvas_uuid: str, optional
                :param scene_name: Name of the scene the item is in
                :type scene_name: str, optional
                :param scene_uuid: UUID of the scene the item is in
                :type scene_uuid: str, optional
                :param scene_item_id: Numeric ID of the scene item
                :type scene_item_id: int
        """
        payload = {
            "canvasUuid": canvas_uuid,
            "sceneName": scene_name,
            "sceneUuid": scene_uuid,
            "sceneItemId": scene_item_id,
        }
        return self.send("GetSceneItemTransform", payload)

    def set_scene_item_transform(
        self,
        *,
        canvas_uuid: Optional[str] = None,
        scene_name: Optional[str] = None,
        scene_uuid: Optional[str] = None,
        scene_item_id: int,
        scene_item_transform: Mapping,
    ):
        """
        Sets the transform and crop info of a scene item.

            :param canvas_uuid: UUID of the canvas the scene is in, if using the sceneName field
            :type canvas_uuid: str, optional
            :param scene_name: Name of the scene the item is in
            :type scene_name: str, optional
            :param scene_uuid: UUID of the scene the item is in
            :type scene_uuid: str, optional
            :param scene_item_id: Numeric ID of the scene item
            :type scene_item_id: int
            :param scene_item_transform: Object containing scene item transform info to update
            :type scene_item_transform: Mapping
        """
        payload = {
            "canvasUuid": canvas_uuid,
            "sceneName": scene_name,
            "sceneUuid": scene_uuid,
            "sceneItemId": scene_item_id,
            "sceneItemTransform": scene_item_transform,
        }
        return self.send("SetSceneItemTransform", payload)

    def get_scene_item_enabled(
        self,
        *,
        canvas_uuid: Optional[str] = None,
        scene_name: Optional[str] = None,
        scene_uuid: Optional[str] = None,
        scene_item_id: int,
    ):
        """
            Gets the enable state of a scene item.

        Scenes and Groups

                :param canvas_uuid: UUID of the canvas the scene is in, if using the sceneName field
                :type canvas_uuid: str, optional
                :param scene_name: Name of the scene the item is in
                :type scene_name: str, optional
                :param scene_uuid: UUID of the scene the item is in
                :type scene_uuid: str, optional
                :param scene_item_id: Numeric ID of the scene item
                :type scene_item_id: int
        """
        payload = {
            "canvasUuid": canvas_uuid,
            "sceneName": scene_name,
            "sceneUuid": scene_uuid,
            "sceneItemId": scene_item_id,
        }
        return self.send("GetSceneItemEnabled", payload)

    def set_scene_item_enabled(
        self,
        *,
        canvas_uuid: Optional[str] = None,
        scene_name: Optional[str] = None,
        scene_uuid: Optional[str] = None,
        scene_item_id: int,
        scene_item_enabled: bool,
    ):
        """
            Sets the enable state of a scene item.

        Scenes and Groups

                :param canvas_uuid: UUID of the canvas the scene is in, if using the sceneName field
                :type canvas_uuid: str, optional
                :param scene_name: Name of the scene the item is in
                :type scene_name: str, optional
                :param scene_uuid: UUID of the scene the item is in
                :type scene_uuid: str, optional
                :param scene_item_id: Numeric ID of the scene item
                :type scene_item_id: int
                :param scene_item_enabled: New enable state of the scene item
                :type scene_item_enabled: bool
        """
        payload = {
            "canvasUuid": canvas_uuid,
            "sceneName": scene_name,
            "sceneUuid": scene_uuid,
            "sceneItemId": scene_item_id,
            "sceneItemEnabled": scene_item_enabled,
        }
        return self.send("SetSceneItemEnabled", payload)

    def get_scene_item_locked(
        self,
        *,
        canvas_uuid: Optional[str] = None,
        scene_name: Optional[str] = None,
        scene_uuid: Optional[str] = None,
        scene_item_id: int,
    ):
        """
            Gets the lock state of a scene item.

        Scenes and Groups

                :param canvas_uuid: UUID of the canvas the scene is in, if using the sceneName field
                :type canvas_uuid: str, optional
                :param scene_name: Name of the scene the item is in
                :type scene_name: str, optional
                :param scene_uuid: UUID of the scene the item is in
                :type scene_uuid: str, optional
                :param scene_item_id: Numeric ID of the scene item
                :type scene_item_id: int
        """
        payload = {
            "canvasUuid": canvas_uuid,
            "sceneName": scene_name,
            "sceneUuid": scene_uuid,
            "sceneItemId": scene_item_id,
        }
        return self.send("GetSceneItemLocked", payload)

    def set_scene_item_locked(
        self,
        *,
        canvas_uuid: Optional[str] = None,
        scene_name: Optional[str] = None,
        scene_uuid: Optional[str] = None,
        scene_item_id: int,
        scene_item_locked: bool,
    ):
        """
            Sets the lock state of a scene item.

        Scenes and Group

                :param canvas_uuid: UUID of the canvas the scene is in, if using the sceneName field
                :type canvas_uuid: str, optional
                :param scene_name: Name of the scene the item is in
                :type scene_name: str, optional
                :param scene_uuid: UUID of the scene the item is in
                :type scene_uuid: str, optional
                :param scene_item_id: Numeric ID of the scene item
                :type scene_item_id: int
                :param scene_item_locked: New lock state of the scene item
                :type scene_item_locked: bool
        """
        payload = {
            "canvasUuid": canvas_uuid,
            "sceneName": scene_name,
            "sceneUuid": scene_uuid,
            "sceneItemId": scene_item_id,
            "sceneItemLocked": scene_item_locked,
        }
        return self.send("SetSceneItemLocked", payload)

    def get_scene_item_index(
        self,
        *,
        canvas_uuid: Optional[str] = None,
        scene_name: Optional[str] = None,
        scene_uuid: Optional[str] = None,
        scene_item_id: int,
    ):
        """
            Gets the index position of a scene item in a scene.

        An index of 0 is at the bottom of the source list in the UI.

        Scenes and Groups

                :param canvas_uuid: UUID of the canvas the scene is in, if using the sceneName field
                :type canvas_uuid: str, optional
                :param scene_name: Name of the scene the item is in
                :type scene_name: str, optional
                :param scene_uuid: UUID of the scene the item is in
                :type scene_uuid: str, optional
                :param scene_item_id: Numeric ID of the scene item
                :type scene_item_id: int
        """
        payload = {
            "canvasUuid": canvas_uuid,
            "sceneName": scene_name,
            "sceneUuid": scene_uuid,
            "sceneItemId": scene_item_id,
        }
        return self.send("GetSceneItemIndex", payload)

    def set_scene_item_index(
        self,
        *,
        canvas_uuid: Optional[str] = None,
        scene_name: Optional[str] = None,
        scene_uuid: Optional[str] = None,
        scene_item_id: int,
        scene_item_index: int,
    ):
        """
            Sets the index position of a scene item in a scene.

        Scenes and Groups

                :param canvas_uuid: UUID of the canvas the scene is in, if using the sceneName field
                :type canvas_uuid: str, optional
                :param scene_name: Name of the scene the item is in
                :type scene_name: str, optional
                :param scene_uuid: UUID of the scene the item is in
                :type scene_uuid: str, optional
                :param scene_item_id: Numeric ID of the scene item
                :type scene_item_id: int
                :param scene_item_index: New index position of the scene item
                :type scene_item_index: int
        """
        payload = {
            "canvasUuid": canvas_uuid,
            "sceneName": scene_name,
            "sceneUuid": scene_uuid,
            "sceneItemId": scene_item_id,
            "sceneItemIndex": scene_item_index,
        }
        return self.send("SetSceneItemIndex", payload)

    def get_scene_item_blend_mode(
        self,
        *,
        canvas_uuid: Optional[str] = None,
        scene_name: Optional[str] = None,
        scene_uuid: Optional[str] = None,
        scene_item_id: int,
    ):
        """
            Gets the blend mode of a scene item.

        Blend modes:

        - `OBS_BLEND_NORMAL`
        - `OBS_BLEND_ADDITIVE`
        - `OBS_BLEND_SUBTRACT`
        - `OBS_BLEND_SCREEN`
        - `OBS_BLEND_MULTIPLY`
        - `OBS_BLEND_LIGHTEN`
        - `OBS_BLEND_DARKEN`

        Scenes and Groups

                :param canvas_uuid: UUID of the canvas the scene is in, if using the sceneName field
                :type canvas_uuid: str, optional
                :param scene_name: Name of the scene the item is in
                :type scene_name: str, optional
                :param scene_uuid: UUID of the scene the item is in
                :type scene_uuid: str, optional
                :param scene_item_id: Numeric ID of the scene item
                :type scene_item_id: int
        """
        payload = {
            "canvasUuid": canvas_uuid,
            "sceneName": scene_name,
            "sceneUuid": scene_uuid,
            "sceneItemId": scene_item_id,
        }
        return self.send("GetSceneItemBlendMode", payload)

    def set_scene_item_blend_mode(
        self,
        *,
        canvas_uuid: Optional[str] = None,
        scene_name: Optional[str] = None,
        scene_uuid: Optional[str] = None,
        scene_item_id: int,
        scene_item_blend_mode: str,
    ):
        """
            Sets the blend mode of a scene item.

        Scenes and Groups

                :param canvas_uuid: UUID of the canvas the scene is in, if using the sceneName field
                :type canvas_uuid: str, optional
                :param scene_name: Name of the scene the item is in
                :type scene_name: str, optional
                :param scene_uuid: UUID of the scene the item is in
                :type scene_uuid: str, optional
                :param scene_item_id: Numeric ID of the scene item
                :type scene_item_id: int
                :param scene_item_blend_mode: New blend mode
                :type scene_item_blend_mode: str
        """
        payload = {
            "canvasUuid": canvas_uuid,
            "sceneName": scene_name,
            "sceneUuid": scene_uuid,
            "sceneItemId": scene_item_id,
            "sceneItemBlendMode": scene_item_blend_mode,
        }
        return self.send("SetSceneItemBlendMode", payload)

    def get_scene_list(self, *, canvas_uuid: Optional[str] = None):
        """
        Gets an array of scenes in OBS.

            :param canvas_uuid: UUID of the canvas the scenes are in
            :type canvas_uuid: str, optional
        """
        payload = {
            "canvasUuid": canvas_uuid,
        }
        return self.send("GetSceneList", payload)

    def get_group_list(self):
        """
            Gets an array of all groups in OBS.

        Groups in OBS are actually scenes, but renamed and modified. In obs-websocket, we treat them as scenes where we can.


        """
        payload = {}
        return self.send("GetGroupList", payload)

    def get_current_program_scene(self):
        """
            Gets the current program scene.

        Note 1: This request is slated to have the `currentProgram`-prefixed fields removed from in an upcoming RPC version.

        Note 2: Canvases do not have any concept of a program or preview scene, so this request does not support canvases.


        """
        payload = {}
        return self.send("GetCurrentProgramScene", payload)

    def set_current_program_scene(
        self, *, scene_name: Optional[str] = None, scene_uuid: Optional[str] = None
    ):
        """
        Sets the current program scene.

            :param scene_name: Scene name to set as the current program scene
            :type scene_name: str, optional
            :param scene_uuid: Scene UUID to set as the current program scene
            :type scene_uuid: str, optional
        """
        payload = {
            "sceneName": scene_name,
            "sceneUuid": scene_uuid,
        }
        return self.send("SetCurrentProgramScene", payload)

    def get_current_preview_scene(self):
        """
            Gets the current preview scene.

        Only available when studio mode is enabled.

        Note: This request is slated to have the `currentPreview`-prefixed fields removed from in an upcoming RPC version.


        """
        payload = {}
        return self.send("GetCurrentPreviewScene", payload)

    def set_current_preview_scene(
        self, *, scene_name: Optional[str] = None, scene_uuid: Optional[str] = None
    ):
        """
            Sets the current preview scene.

        Only available when studio mode is enabled.

                :param scene_name: Scene name to set as the current preview scene
                :type scene_name: str, optional
                :param scene_uuid: Scene UUID to set as the current preview scene
                :type scene_uuid: str, optional
        """
        payload = {
            "sceneName": scene_name,
            "sceneUuid": scene_uuid,
        }
        return self.send("SetCurrentPreviewScene", payload)

    def create_scene(self, *, canvas_uuid: Optional[str] = None, scene_name: str):
        """
        Creates a new scene in OBS.

            :param canvas_uuid: UUID of the canvas to create the new scene in. Leave default to assume main canvas
            :type canvas_uuid: str, optional
            :param scene_name: Name for the new scene
            :type scene_name: str
        """
        payload = {
            "canvasUuid": canvas_uuid,
            "sceneName": scene_name,
        }
        return self.send("CreateScene", payload)

    def remove_scene(
        self,
        *,
        canvas_uuid: Optional[str] = None,
        scene_name: Optional[str] = None,
        scene_uuid: Optional[str] = None,
    ):
        """
        Removes a scene from OBS.

            :param canvas_uuid: UUID of the canvas the scene is in, if using the sceneName field
            :type canvas_uuid: str, optional
            :param scene_name: Name of the scene to remove
            :type scene_name: str, optional
            :param scene_uuid: UUID of the scene to remove
            :type scene_uuid: str, optional
        """
        payload = {
            "canvasUuid": canvas_uuid,
            "sceneName": scene_name,
            "sceneUuid": scene_uuid,
        }
        return self.send("RemoveScene", payload)

    def set_scene_name(
        self,
        *,
        canvas_uuid: Optional[str] = None,
        scene_name: Optional[str] = None,
        scene_uuid: Optional[str] = None,
        new_scene_name: str,
    ):
        """
        Sets the name of a scene (rename).

            :param canvas_uuid: UUID of the canvas the scene is in, if using the sceneName field
            :type canvas_uuid: str, optional
            :param scene_name: Name of the scene to be renamed
            :type scene_name: str, optional
            :param scene_uuid: UUID of the scene to be renamed
            :type scene_uuid: str, optional
            :param new_scene_name: New name for the scene
            :type new_scene_name: str
        """
        payload = {
            "canvasUuid": canvas_uuid,
            "sceneName": scene_name,
            "sceneUuid": scene_uuid,
            "newSceneName": new_scene_name,
        }
        return self.send("SetSceneName", payload)

    def get_scene_scene_transition_override(
        self,
        *,
        canvas_uuid: Optional[str] = None,
        scene_name: Optional[str] = None,
        scene_uuid: Optional[str] = None,
    ):
        """
            Gets the scene transition overridden for a scene.

        Note: A transition UUID response field is not currently able to be implemented as of 2024-1-18.

                :param canvas_uuid: UUID of the canvas the scene is in, if using the sceneName field
                :type canvas_uuid: str, optional
                :param scene_name: Name of the scene
                :type scene_name: str, optional
                :param scene_uuid: UUID of the scene
                :type scene_uuid: str, optional
        """
        payload = {
            "canvasUuid": canvas_uuid,
            "sceneName": scene_name,
            "sceneUuid": scene_uuid,
        }
        return self.send("GetSceneSceneTransitionOverride", payload)

    def set_scene_scene_transition_override(
        self,
        *,
        canvas_uuid: Optional[str] = None,
        scene_name: Optional[str] = None,
        scene_uuid: Optional[str] = None,
        transition_name: Optional[str] = None,
        transition_duration: Optional[int] = None,
    ):
        """
        Sets the scene transition overridden for a scene.

            :param canvas_uuid: UUID of the canvas the scene is in, if using the sceneName field
            :type canvas_uuid: str, optional
            :param scene_name: Name of the scene
            :type scene_name: str, optional
            :param scene_uuid: UUID of the scene
            :type scene_uuid: str, optional
            :param transition_name: Name of the scene transition to use as override. Specify `null` to remove
            :type transition_name: str, optional
            :param transition_duration: Duration to use for any overridden transition. Specify `null` to remove
            :type transition_duration: int, optional
        """
        payload = {
            "canvasUuid": canvas_uuid,
            "sceneName": scene_name,
            "sceneUuid": scene_uuid,
            "transitionName": transition_name,
            "transitionDuration": transition_duration,
        }
        return self.send("SetSceneSceneTransitionOverride", payload)

    def get_source_active(
        self,
        *,
        canvas_uuid: Optional[str] = None,
        source_name: Optional[str] = None,
        source_uuid: Optional[str] = None,
    ):
        """
            Gets the active and show state of a source.

        **Compatible with inputs and scenes.**

                :param canvas_uuid: UUID of the canvas the source is in, if using sourceName field
                :type canvas_uuid: str, optional
                :param source_name: Name of the source to get the active state of
                :type source_name: str, optional
                :param source_uuid: UUID of the source to get the active state of
                :type source_uuid: str, optional
        """
        payload = {
            "canvasUuid": canvas_uuid,
            "sourceName": source_name,
            "sourceUuid": source_uuid,
        }
        return self.send("GetSourceActive", payload)

    def get_source_screenshot(
        self,
        *,
        canvas_uuid: Optional[str] = None,
        source_name: Optional[str] = None,
        source_uuid: Optional[str] = None,
        image_format: str,
        image_width: Optional[int] = None,
        image_height: Optional[int] = None,
        image_compression_quality: Optional[int] = -1,
    ):
        """
            Gets a Base64-encoded screenshot of a source.

        The `imageWidth` and `imageHeight` parameters are treated as "scale to inner", meaning the smallest ratio will be used and the aspect ratio of the original resolution is kept.
        If `imageWidth` and `imageHeight` are not specified, the compressed image will use the full resolution of the source.

        **Compatible with inputs and scenes.**

                :param canvas_uuid: UUID of the canvas the source is in, if using sourceName field
                :type canvas_uuid: str, optional
                :param source_name: Name of the source to take a screenshot of
                :type source_name: str, optional
                :param source_uuid: UUID of the source to take a screenshot of
                :type source_uuid: str, optional
                :param image_format: Image compression format to use. Use `GetVersion` to get compatible image formats
                :type image_format: str
                :param image_width: Width to scale the screenshot to
                :type image_width: int, optional
                :param image_height: Height to scale the screenshot to
                :type image_height: int, optional
                :param image_compression_quality: Compression quality to use. 0 for high compression, 100 for uncompressed. -1 to use "default" (whatever that means, idk)
                :type image_compression_quality: int, optional
        """
        payload = {
            "canvasUuid": canvas_uuid,
            "sourceName": source_name,
            "sourceUuid": source_uuid,
            "imageFormat": image_format,
            "imageWidth": image_width,
            "imageHeight": image_height,
            "imageCompressionQuality": image_compression_quality,
        }
        return self.send("GetSourceScreenshot", payload)

    def save_source_screenshot(
        self,
        *,
        canvas_uuid: Optional[str] = None,
        source_name: Optional[str] = None,
        source_uuid: Optional[str] = None,
        image_format: str,
        image_file_path: str,
        image_width: Optional[int] = None,
        image_height: Optional[int] = None,
        image_compression_quality: Optional[int] = -1,
    ):
        """
            Saves a screenshot of a source to the filesystem.

        The `imageWidth` and `imageHeight` parameters are treated as "scale to inner", meaning the smallest ratio will be used and the aspect ratio of the original resolution is kept.
        If `imageWidth` and `imageHeight` are not specified, the compressed image will use the full resolution of the source.

        **Compatible with inputs and scenes.**

                :param canvas_uuid: UUID of the canvas the source is in, if using sourceName field
                :type canvas_uuid: str, optional
                :param source_name: Name of the source to take a screenshot of
                :type source_name: str, optional
                :param source_uuid: UUID of the source to take a screenshot of
                :type source_uuid: str, optional
                :param image_format: Image compression format to use. Use `GetVersion` to get compatible image formats
                :type image_format: str
                :param image_file_path: Path to save the screenshot file to. Eg. `C:/Users/user/Desktop/screenshot.png`
                :type image_file_path: str
                :param image_width: Width to scale the screenshot to
                :type image_width: int, optional
                :param image_height: Height to scale the screenshot to
                :type image_height: int, optional
                :param image_compression_quality: Compression quality to use. 0 for high compression, 100 for uncompressed. -1 to use "default" (whatever that means, idk)
                :type image_compression_quality: int, optional
        """
        payload = {
            "canvasUuid": canvas_uuid,
            "sourceName": source_name,
            "sourceUuid": source_uuid,
            "imageFormat": image_format,
            "imageFilePath": image_file_path,
            "imageWidth": image_width,
            "imageHeight": image_height,
            "imageCompressionQuality": image_compression_quality,
        }
        return self.send("SaveSourceScreenshot", payload)

    def get_stream_status(self):
        """
        Gets the status of the stream output.


        """
        payload = {}
        return self.send("GetStreamStatus", payload)

    def toggle_stream(self):
        """
        Toggles the status of the stream output.


        """
        payload = {}
        return self.send("ToggleStream", payload)

    def start_stream(self):
        """
        Starts the stream output.


        """
        payload = {}
        return self.send("StartStream", payload)

    def stop_stream(self):
        """
        Stops the stream output.


        """
        payload = {}
        return self.send("StopStream", payload)

    def send_stream_caption(self, *, caption_text: str):
        """
        Sends CEA-608 caption text over the stream output.

            :param caption_text: Caption text
            :type caption_text: str
        """
        payload = {
            "captionText": caption_text,
        }
        return self.send("SendStreamCaption", payload)

    def get_transition_kind_list(self):
        """
            Gets an array of all available transition kinds.

        Similar to `GetInputKindList`


        """
        payload = {}
        return self.send("GetTransitionKindList", payload)

    def get_scene_transition_list(self):
        """
        Gets an array of all scene transitions in OBS.


        """
        payload = {}
        return self.send("GetSceneTransitionList", payload)

    def get_current_scene_transition(self):
        """
        Gets information about the current scene transition.


        """
        payload = {}
        return self.send("GetCurrentSceneTransition", payload)

    def set_current_scene_transition(self, *, transition_name: str):
        """
            Sets the current scene transition.

        Small note: While the namespace of scene transitions is generally unique, that uniqueness is not a guarantee as it is with other resources like inputs.

                :param transition_name: Name of the transition to make active
                :type transition_name: str
        """
        payload = {
            "transitionName": transition_name,
        }
        return self.send("SetCurrentSceneTransition", payload)

    def set_current_scene_transition_duration(self, *, transition_duration: int):
        """
        Sets the duration of the current scene transition, if it is not fixed.

            :param transition_duration: Duration in milliseconds
            :type transition_duration: int
        """
        payload = {
            "transitionDuration": transition_duration,
        }
        return self.send("SetCurrentSceneTransitionDuration", payload)

    def set_current_scene_transition_settings(
        self, *, transition_settings: Mapping, overlay: Optional[bool] = True
    ):
        """
        Sets the settings of the current scene transition.

            :param transition_settings: Settings object to apply to the transition. Can be `{}`
            :type transition_settings: Mapping
            :param overlay: Whether to overlay over the current settings or replace them
            :type overlay: bool, optional
        """
        payload = {
            "transitionSettings": transition_settings,
            "overlay": overlay,
        }
        return self.send("SetCurrentSceneTransitionSettings", payload)

    def get_current_scene_transition_cursor(self):
        """
            Gets the cursor position of the current scene transition.

        Note: `transitionCursor` will return 1.0 when the transition is inactive.


        """
        payload = {}
        return self.send("GetCurrentSceneTransitionCursor", payload)

    def trigger_studio_mode_transition(self):
        """
        Triggers the current scene transition. Same functionality as the `Transition` button in studio mode.


        """
        payload = {}
        return self.send("TriggerStudioModeTransition", payload)

    def set_t_bar_position(self, *, position: int, release: Optional[bool] = None):
        """
            Sets the position of the TBar.

        **Very important note**: This will be deprecated and replaced in a future version of obs-websocket.

                :param position: New position
                :type position: int
                :param release: Whether to release the TBar. Only set `false` if you know that you will be sending another position update
                :type release: bool, optional
        """
        warn(
            "set_t_bar_position: **Very important note**: This will be deprecated and replaced in a future version of obs-websocket.",
            DeprecationWarning,
            stacklevel=2,
        )
        payload = {
            "position": position,
            "release": release,
        }
        return self.send("SetTBarPosition", payload)

    def get_studio_mode_enabled(self):
        """
        Gets whether studio is enabled.


        """
        payload = {}
        return self.send("GetStudioModeEnabled", payload)

    def set_studio_mode_enabled(self, *, studio_mode_enabled: bool):
        """
        Enables or disables studio mode

            :param studio_mode_enabled: True == Enabled, False == Disabled
            :type studio_mode_enabled: bool
        """
        payload = {
            "studioModeEnabled": studio_mode_enabled,
        }
        return self.send("SetStudioModeEnabled", payload)

    def open_input_properties_dialog(
        self, *, input_name: Optional[str] = None, input_uuid: Optional[str] = None
    ):
        """
        Opens the properties dialog of an input.

            :param input_name: Name of the input to open the dialog of
            :type input_name: str, optional
            :param input_uuid: UUID of the input to open the dialog of
            :type input_uuid: str, optional
        """
        payload = {
            "inputName": input_name,
            "inputUuid": input_uuid,
        }
        return self.send("OpenInputPropertiesDialog", payload)

    def open_input_filters_dialog(
        self, *, input_name: Optional[str] = None, input_uuid: Optional[str] = None
    ):
        """
        Opens the filters dialog of an input.

            :param input_name: Name of the input to open the dialog of
            :type input_name: str, optional
            :param input_uuid: UUID of the input to open the dialog of
            :type input_uuid: str, optional
        """
        payload = {
            "inputName": input_name,
            "inputUuid": input_uuid,
        }
        return self.send("OpenInputFiltersDialog", payload)

    def open_input_interact_dialog(
        self, *, input_name: Optional[str] = None, input_uuid: Optional[str] = None
    ):
        """
        Opens the interact dialog of an input.

            :param input_name: Name of the input to open the dialog of
            :type input_name: str, optional
            :param input_uuid: UUID of the input to open the dialog of
            :type input_uuid: str, optional
        """
        payload = {
            "inputName": input_name,
            "inputUuid": input_uuid,
        }
        return self.send("OpenInputInteractDialog", payload)

    def get_monitor_list(self):
        """
        Gets a list of connected monitors and information about them.


        """
        payload = {}
        return self.send("GetMonitorList", payload)

    def open_video_mix_projector(
        self,
        *,
        video_mix_type: str,
        monitor_index: Optional[int] = -1,
        projector_geometry: Optional[str] = None,
    ):
        """
            Opens a projector for a specific output video mix.

        Mix types:

        - `OBS_WEBSOCKET_VIDEO_MIX_TYPE_PREVIEW`
        - `OBS_WEBSOCKET_VIDEO_MIX_TYPE_PROGRAM`
        - `OBS_WEBSOCKET_VIDEO_MIX_TYPE_MULTIVIEW`

        Note: This request serves to provide feature parity with 4.x. It is very likely to be changed/deprecated in a future release.

                :param video_mix_type: Type of mix to open
                :type video_mix_type: str
                :param monitor_index: Monitor index, use `GetMonitorList` to obtain index
                :type monitor_index: int, optional
                :param projector_geometry: Size/Position data for a windowed projector, in Qt Base64 encoded format. Mutually exclusive with `monitorIndex`
                :type projector_geometry: str, optional
        """
        warn(
            "open_video_mix_projector: This request serves to provide feature parity with 4.x. It is very likely to be changed/deprecated in a future release.",
            DeprecationWarning,
            stacklevel=2,
        )
        payload = {
            "videoMixType": video_mix_type,
            "monitorIndex": monitor_index,
            "projectorGeometry": projector_geometry,
        }
        return self.send("OpenVideoMixProjector", payload)

    def open_source_projector(
        self,
        *,
        canvas_uuid: Optional[str] = None,
        source_name: Optional[str] = None,
        source_uuid: Optional[str] = None,
        monitor_index: Optional[int] = -1,
        projector_geometry: Optional[str] = None,
    ):
        """
            Opens a projector for a source.

        Note: This request serves to provide feature parity with 4.x. It is very likely to be changed/deprecated in a future release.

                :param canvas_uuid: UUID of the canvas the source is in, if using the sourceName field
                :type canvas_uuid: str, optional
                :param source_name: Name of the source to open a projector for
                :type source_name: str, optional
                :param source_uuid: UUID of the source to open a projector for
                :type source_uuid: str, optional
                :param monitor_index: Monitor index, use `GetMonitorList` to obtain index
                :type monitor_index: int, optional
                :param projector_geometry: Size/Position data for a windowed projector, in Qt Base64 encoded format. Mutually exclusive with `monitorIndex`
                :type projector_geometry: str, optional
        """
        warn(
            "open_source_projector: This request serves to provide feature parity with 4.x. It is very likely to be changed/deprecated in a future release.",
            DeprecationWarning,
            stacklevel=2,
        )
        payload = {
            "canvasUuid": canvas_uuid,
            "sourceName": source_name,
            "sourceUuid": source_uuid,
            "monitorIndex": monitor_index,
            "projectorGeometry": projector_geometry,
        }
        return self.send("OpenSourceProjector", payload)
