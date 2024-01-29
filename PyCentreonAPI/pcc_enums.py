from enum import Enum


class HostParameters(Enum):
    def __str__(self):
        return self.value

    GEO_COORDS = "geo_coords"
    COORDS_2D = "2d_coords"
    COORDS_3D = "3d_coords"
    ACTION_URL = "action_url"
    ACTIVATE = "activate"
    ACTIVE_CHECKS_ENABLED = "active_checks_enabled"
    ACKNOWLEDGEMENT_TIMEOUT = "acknowledgement_timeout"
    ADDRESS = "address"
    ALIAS = "alias"
    CHECK_COMMAND = "check_command"
    CHECK_COMMAND_ARGUMENTS = "check_command_arguments"
    CHECK_INTERVAL = "check_interval"
    CHECK_FRESHNESS = "check_freshness"
    CHECK_PERIOD = "check_period"
    CONTACT_ADDITIVE_INHERITANCE = "contact_additive_inheritance"
    CG_ADDITIVE_INHERITANCE = "cg_additive_inheritance"
    EVENT_HANDLER = "event_handler"
    EVENT_HANDLER_ARGUMENTS = "event_handler_arguments"
    EVENT_HANDLER_ENABLED = "event_handler_enabled"
    FIRST_NOTIFICATION_DELAY = "first_notification_delay"
    FLAP_DETECTION_ENABLED = "flap_detection_enabled"
    FLAP_DETECTION_OPTIONS = "flap_detection_options"
    HOST_HIGH_FLAP_THRESHOLD = "host_high_flap_threshold"
    HOST_LOW_FLAP_THRESHOLD = "host_low_flap_threshold"
    ICON_IMAGE = "icon_image"
    ICON_IMAGE_ALT = "icon_image_alt"
    MAX_CHECK_ATTEMPTS = "max_check_attempts"
    NAME = "name"
    NOTES = "notes"
    NOTES_URL = "notes_url"
    NOTIFICATIONS_ENABLED = "notifications_enabled"
    NOTIFICATION_INTERVAL = "notification_interval"
    NOTIFICATION_OPTIONS = "notification_options"
    NOTIFICATION_PERIOD = "notification_period"
    RECOVERY_NOTIFICATION_DELAY = "recovery_notification_delay"
    OBSESS_OVER_HOST = "obsess_over_host"
    PASSIVE_CHECKS_ENABLED = "passive_checks_enabled"
    RETAIN_NONSTATUS_INFORMATION = "retain_nonstatus_information"
    RETAIN_STATUS_INFORMATION = "retain_status_information"
    RETRY_CHECK_INTERVAL = "retry_check_interval"
    SNMP_COMMUNITY = "snmp_community"
    SNMP_VERSION = "snmp_version"
    STALKING_OPTIONS = "stalking_options"
    STATUSMAP_IMAGE = "statusmap_image"
    HOST_NOTIFICATION_OPTIONS = "host_notification_options"
    TIMEZONE = "timezone"
    COMMENT = "comment"


class GorgoneCommType(Enum):
    def __str__(self):
        return self.value

    ZMQ = "1"
    SSH = "2"


class PollerParameters(Enum):
    def __str__(self):
        return self.value

    NAME = "name"
    LOCALHOST = "localhost"
    NS_IP_ADDRESS = "ns_ip_address"
    NS_ACTIVATE = "ns_activate"
    ENGINE_START_COMMAND = "engine_start_command"
    ENGINE_STOP_COMMAND = "engine_stop_command"
    ENGINE_RESTART_COMMAND = "engine_restart_command"
    ENGINE_RELOAD_COMMAND = "engine_reload_command"
    NAGIOS_BIN = "nagios_bin"
    NAGIOSTATS_BIN = "nagiostats_bin"
    SSH_PORT = "ssh_port"
    BROKER_RELOAD_COMMAND = "broker_reload_command"
    CENTREONBROKER_CFG_PATH = "centreonbroker_cfg_path"
    CENTREONBROKER_MODULE_PATH = "centreonbroker_module_path"


class ServiceParameters(Enum):
    def __str__(self):
        return self.value

    ACTIVATE = "activate"
    DESCRIPTION = "description"
    TEMPLATE = "template"
    IS_VOLATILE = "is_volatile"
    CHECK_PERIOD = "check_period"
    CHECK_COMMAND = "check_command"
    CHECK_COMMAND_ARGUMENTS = "check_command_arguments"
    MAX_CHECK_ATTEMPTS = "max_check_attempts"
    NORMAL_CHECK_INTERVAL = "normal_check_interval"
    RETRY_CHECK_INTERVAL = "retry_check_interval"
    ACTIVE_CHECKS_ENABLED = "active_checks_enabled"
    PASSIVE_CHECKS_ENABLED = "passive_checks_enabled"
    NOTIFICATIONS_ENABLED = "notifications_enabled"
    CONTACT_ADDITIVE_INHERITANCE = "contact_additive_inheritance"
    CG_ADDITIVE_INHERITANCE = "cg_additive_inheritance"
    NOTIFICATION_INTERVAL = "notification_interval"
    NOTIFICATION_PERIOD = "notification_period"
    NOTIFICATION_OPTIONS = "notification_options"
    FIRST_NOTIFICATION_DELAY = "first_notification_delay"
    RECOVERY_NOTIFICATION_DELAY = "recovery_notification_delay"
    OBSESS_OVER_SERVICE = "obsess_over_service"
    CHECK_FRESHNESS = "check_freshness"
    FRESHNESS_THRESHOLD = "freshness_threshold"
    EVENT_HANDLER_ENABLED = "event_handler_enabled"
    FLAP_DETECTION_ENABLED = "flap_detection_enabled"
    RETAIN_STATUS_INFORMATION = "retain_status_information"
    RETAIN_NONSTATUS_INFORMATION = "retain_nonstatus_information"
    EVENT_HANDLER = "event_handler"
    EVENT_HANDLER_ARGUMENTS = "event_handler_arguments"
    NOTES = "notes"
    NOTES_URL = "notes_url"
    ACTION_URL = "action_url"
    ICON_IMAGE = "icon_image"
    ICON_IMAGE_ALT = "icon_image_alt"
    COMMENT = "comment"
    SERVICE_NOTIFICATION_OPTIONS = "service_notification_options"


