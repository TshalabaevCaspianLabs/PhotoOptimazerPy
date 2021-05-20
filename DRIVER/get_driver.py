import os
import random
import zipfile

from loguru import logger
from selenium import webdriver




def get_chromedriver(use_proxy=False, mobile=False):
    proxyes = [
        ['176.222.57.238', '54732', 'CcGkyCgj', 'c4YEiULZ'],
        ['212.60.7.69', '49531', 'CcGkyCgj', 'c4YEiULZ'],
        ['45.93.80.180', '55601', 'CcGkyCgj', 'c4YEiULZ'],
        ['45.149.129.151', '54549', 'CcGkyCgj', 'c4YEiULZ']
    ]
    proxy = random.choice(proxyes)


    PROXY_HOST = proxy[0]
    PROXY_PORT = proxy[1]
    PROXY_USER = proxy[2]
    PROXY_PASS = proxy[3]

    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """
    background_js = """
    var config = {
            mode: "fixed_servers",
            rules: {
            singleProxy: {
                scheme: "http",
                host: "%s",
                port: parseInt(%s)
            },
            bypassList: ["localhost"]
            }
        };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)



    path = os.path.dirname(os.path.abspath(__file__))
    chrome_options = webdriver.ChromeOptions()
    if use_proxy:
        pluginfile = 'proxy_auth_plugin.zip'

        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        chrome_options.add_extension(pluginfile)

    if mobile:
        mobile_list = [{"deviceName": "iPhone 6"}, {"deviceName": "iPhone X"},
                       {"deviceName": "iPhone 7"}, {"deviceName": "iPhone 8"}, {"deviceName": "iPhone 5"},
                       {"deviceName": "iPhone SE"}]

        mobile_emulation = random.choice(mobile_list)
        logger.info(mobile_emulation['deviceName'])
        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    preferences = {
            "webrtc.ip_handling_policy": "disable_non_proxied_udp",
            "webrtc.multiple_routes_enabled": False,
            "webrtc.nonproxied_udp_enabled": False,
            "download.default_directory": "/Users/macbookpro/Documents/PhotoOptimazerPy/PHOTO/DOWNLOAD",
            "download.prompt_for_download": False,
            "download.directory_upgrade": True
        }
    chrome_options.add_experimental_option("prefs", preferences)
    params = {
        "latitude": 53.1785,
        "longitude": 50.1267,
        "accuracy": 100
    }
    driver = webdriver.Chrome(
        '/Users/macbookpro/Documents/AvitoPy/DRIVER/chromedriver',
        chrome_options=chrome_options)
    driver.execute_cdp_cmd("Page.setGeolocationOverride", params)
    return driver
