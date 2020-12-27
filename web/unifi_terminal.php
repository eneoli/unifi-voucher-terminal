<?php

require_once('lib/unifi_client.php');

// Config
const TOKEN = "TEST";
const USER = "admin";
const PASSWORD = "admin";
const CONTROLLER_URL = "https://localhost:8443";
const SITE_ID = "default";
const CONTROLLER_VERSION = "6.0.41";

const VOUCHER_EXPIRATION = 2000;
const VOUCHER_USERS = 30;
const QRCODE_DATA = "WIFI:S:WLAN am Leo;T:WPA;P:GymnasiumLeoninum";
const PREPENDIX = "Gymnasium Leoninum Handrup \n Dauer: 2 Std. \n SSID: WLAN am Leo \n Passwort: GymnasiumLeoninum";
const APPENDIX = "Viel Spass im Wlan";

header('Content-Type: application/json');

function send_error($header, $msg)
{
    header($header);
    echo(json_encode(["error" => $msg], JSON_PRETTY_PRINT));
}

if (isset($_POST) && strcmp($_POST['token'], TOKEN) == 0) {
    $unifi_connection = new UniFi_API\Client(USER, PASSWORD, CONTROLLER_URL, SITE_ID, CONTROLLER_VERSION);
    $loginresults = $unifi_connection->login();

    if ($loginresults !== true) {
        send_error("HTTP/1.1 401 Unauthorized", "Unifi Login fehlgeschlagen." . ($loginresults ? ('Login-Fehler: ' . $loginresults) : ''));
        return;
    }

    $voucher_result = $unifi_connection->create_voucher(VOUCHER_EXPIRATION, 1, VOUCHER_USERS);
    $vouchers = $unifi_connection->stat_voucher($voucher_result[0]->create_time);

    echo(json_encode([
        "voucher" => $vouchers[0]->code,
        "qrcodeData" => QRCODE_DATA,
        "prependix" => PREPENDIX,
        "appendix" => APPENDIX
    ], JSON_PRETTY_PRINT));
} else {
    send_error('HTTP/1.1 401 Unauthorized', 'API Token nicht korrekt.');
}
