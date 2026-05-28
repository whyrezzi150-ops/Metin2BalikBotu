[app]
title = Metin2 Balik Botu
package.name = balikbotu
package.domain = com.metin2

source.dir = .
source.include_exts = py,png,jpg,kv,xml

version = 1.0.0

requirements = kivy,pillow,pyjnius

android.api = 34
android.minapi = 21

android.permissions = SYSTEM_ALERT_WINDOW,FOREGROUND_SERVICE,INTERNET

orientation = landscape
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1
