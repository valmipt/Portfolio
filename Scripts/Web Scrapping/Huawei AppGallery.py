import aiohttp
import aiofiles
import asyncio
import requests
import json

from aiocsv import AsyncWriter

base_appgallery_url = "https://store-drru.hispace.dbankcloud.ru/hwmarket/api/clientApi"

categories_req_body = "apsid=1676914862678&arkMaxVersion=0&arkMinVersion=0&arkSupport=0&brand=google&channelId" \
                      "=background&clientPackage=com.huawei.appmarket&cno=4010001&code=0200&contentPkg" \
                      "=&dataFilterSwitch=&deviceId=0aa3ba61d395d5f24020f71b56c6e5ef02d1bffd3871016f2f037af24ae10b84" \
                      "&deviceIdRealType=4&deviceIdType=9&deviceSpecParams=%7B%22abis%22%3A%22arm64-v8a%2Carmeabi-v7a" \
                      "%2Carmeabi%22%2C%22deviceFeatures%22%3A%22U%2CP%2C1O%2CB%2C0c%2Ce%2C0J%2Cp%2Ca%2Cb%2C04%2Cm" \
                      "%2C1M%2C08%2C03%2CS%2C0G%2C1Q%2Cq%2C1F%2CL%2C2%2C6%2CY%2CZ%2C1P%2C0M%2C1G%2Cf%2C1%2C07%2C8%2C9" \
                      "%2C1H%2C1I%2CO%2CH%2C0E%2CW%2Cx%2CG%2Co%2C06%2C3%2CR%2Cd%2CQ%2Cn%2Cy%2CT%2Ci%2Cr%2Cu%2Cl%2C4" \
                      "%2CN%2CM%2C01%2C09%2CV%2C7%2C5%2C0H%2Cg%2Cs%2Cc%2CF%2Ct%2C0L%2C0W%2C1N%2C0X%2Ck%2C00%2Cz%2C19" \
                      "%2CK%2C0K%2CE%2C02%2CI%2C1E%2CJ%2Cj%2CD%2Ch%2C1L%2C05%2C1A%2CX%2Cv%2C0e%2Ccom.verizon.hardware" \
                      ".telephony.lte%2Ccom.verizon.hardware.telephony.ehrpd%2Ccom.google.android.feature" \
                      ".D2D_CABLE_MIGRATION_FEATURE%2Candroid.hardware.reboot_escrow%2Ccom.google.android.feature" \
                      ".PIXEL_2017_EXPERIENCE%2Ccom.google.android.feature.PIXEL_2018_EXPERIENCE%2Ccom.google.android" \
                      ".feature.PIXEL_2019_EXPERIENCE%2Ccom.google.android.feature.GOOGLE_BUILD%2Candroid.software" \
                      ".opengles.deqp.level%2Candroid.hardware.sensor.hifi_sensors%2Ccom.google.android.apps.photos" \
                      ".PIXEL_2019_PRELOAD%2Ccom.google.android.feature.TURBO_PRELOAD%2Candroid.hardware.context_hub" \
                      "%2Ccom.google.android.feature.PIXEL_EXPERIENCE%2Ccom.google.android.feature.GOOGLE_FI_BUNDLED" \
                      "%2Candroid.hardware.telephony.carrierlock%2Ccom.google.android.feature.WELLBEING%2Candroid" \
                      ".hardware.device_unique_attestation%2Candroid.software.device_id_attestation%2Ccom.google" \
                      ".android.feature.AER_OPTIMIZED%2Ccom.google.android.feature.NEXT_GENERATION_ASSISTANT%2Ccom" \
                      ".google.android.feature.PIXEL_2019_MIDYEAR_EXPERIENCE%2Ccom.google.android.apps.dialer" \
                      ".SUPPORTED%2Candroid.hardware.identity_credential%2Ccom.google.android.feature" \
                      ".GOOGLE_EXPERIENCE%2Ccom.google.android.feature.EXCHANGE_6_2%2Candroid.hardware.sensor.assist" \
                      "%2Ccom.google.android.feature.DREAMLINER%2Ccom.google.android.feature.ADAPTIVE_CHARGING%22%2C" \
                      "%22dpi%22%3A560%2C%22openglExts%22%3A%221%2C0y%2C1d%2C1e%2C1f%2C0c%2CM%2CO%2C0q%2C0r%2C0s%2CB" \
                      "%2CA%2C5%2C4%2C0p%2CD%2CE%2C0m%2C0n%2C7%2C0i%2C0j%2C0k%2C8%2C0t%2C0w%2C1g%2C1o%2C1m%2C1n%2CH" \
                      "%2C0u%2C1i%2C1l%22%2C%22preferLan%22%3A%22en%22%2C%22usesLibrary%22%3A%225%2C6%2C4%2C2l%2C1H" \
                      "%2CG%2C2m%2C10%2C3%2C09%2C0r%2CA%2C0U%2C9%2C28%2C2%2Cb%2C0Q%2CE%2C0I%2C0J%2C08%2C7%2Cd%2C0V" \
                      "%2CD%2CB%2CC%2C0X%2C0Y%2C0Z%2Ccom.vzw.apnlib%2Ccom.android.hotwordenrollment.common.util" \
                      "%2Cgoogle-ril%2Ccom.android.omadm.radioconfig%2Ccom.qualcomm.qmapbridge%2Clibairbrush-pixel.so" \
                      "%2Ccom.google.android.camera.experimental2019%2ClibOpenCL-pixel.so%2Clib_aion_buffer.so" \
                      "%2ClibqdMetaData.so%2Ccom.google.android.dialer.support%2Ccom.google.android.camera.extensions" \
                      "%2Ccom.google.android.hardwareinfo%2Cqti-telephony-hidl-wrapper-prd%22%7D&fid=0&gaid=2624c0c0" \
                      "-ee52-489b-b6fd-0bf7c06aec4e&globalTrace=null&gradeLevel=0&gradeType=&hardwareType=0" \
                      "&isSupportPage=1&manufacturer=Google&maxResults=25&method=client.getTabDetail&net=1&oaidTrack" \
                      "=1&osv=12&outside=0&recommendSwitch=0&reqPageNum=1&roamingTime=0&runMode=2&serviceType=0" \
                      "&shellApkVer=0&sid=1676914873459&sign" \
                      "=s90035901q0001042000001007u003500a0000000600100000011280000010000050240b0000011000" \
                      "%4008D60505D236459CAA43754B067735DC&thirdPartyPkg=com.huawei.appmarket&translateFlag=1&ts" \
                      "=1676914880572&uri=47cad033194f4183860e8fad8e09fd33%3Faglocation%3D%257B%2522cres%2522%253A" \
                      "%257B%2522lPos%2522%253A0%252C%2522lid%2522%253A%2522903867%2522%252C%2522pos%2522%253A0%252C" \
                      "%2522resid%2522%253A%252247cad033194f4183860e8fad8e09fd33%2522%252C%2522rest%2522%253A%2522tab" \
                      "%2522%252C%2522tid%2522%253A%2522dist_af0f17306bf141c8949f5d1f23e9a112%2522%257D%252C%2522ftid" \
                      "%2522%253A%2522dist_af0f17306bf141c8949f5d1f23e9a112%2522%252C%2522pres%2522%253A%257B" \
                      "%2522lPos%2522%253A0%252C%2522pos%2522%253A2%252C%2522resid%2522%253A" \
                      "%2522af0f17306bf141c8949f5d1f23e9a112%2522%252C%2522rest%2522%253A%2522tab%2522%252C%2522tid" \
                      "%2522%253A%2522dist_af0f17306bf141c8949f5d1f23e9a112%2522%257D%257D%26templateId" \
                      "%3D871221ec262b45b89011bb154fb9af46%26requestId%3D24363a965bd0474fa0ca38880c660c7b" \
                      "%26aglocation%3D%257B%2522cres%2522%253A%257B%2522lPos%2522%253A19%252C%2522lid%2522%253A" \
                      "%2522903867%2522%252C%2522pos%2522%253A0%252C%2522resid%2522%253A%2522Categories%2522%252C" \
                      "%2522rest%2522%253A%2522tab%2522%252C%2522tid%2522%253A" \
                      "%2522dist_af0f17306bf141c8949f5d1f23e9a112%2522%257D%252C%2522ftid%2522%253A" \
                      "%2522dist_af0f17306bf141c8949f5d1f23e9a112%2522%252C%2522pres%2522%253A%257B%2522lPos%2522" \
                      "%253A0%252C%2522pos%2522%253A2%252C%2522resid%2522%253A%2522af0f17306bf141c8949f5d1f23e9a112" \
                      "%2522%252C%2522rest%2522%253A%2522tab%2522%252C%2522tid%2522%253A" \
                      "%2522dist_af0f17306bf141c8949f5d1f23e9a112%2522%257D%257D&ver=1.1 "

categories_content_req_body = "apsid=1676914862678&arkMaxVersion=0&arkMinVersion=0&arkSupport=0&brand=google" \
                              "&channelId=background&clientPackage=com.huawei.appmarket&cno=4010001&code=0200" \
                              "&contentPkg=&dataFilterSwitch=&deviceId" \
                              "=0aa3ba61d395d5f24020f71b56c6e5ef02d1bffd3871016f2f037af24ae10b84&deviceIdRealType=4" \
                              "&deviceIdType=9&deviceSpecParams=%7B%22abis%22%3A%22arm64-v8a%2Carmeabi-v7a%2Carmeabi" \
                              "%22%2C%22deviceFeatures%22%3A%22U%2CP%2C1O%2CB%2C0c%2Ce%2C0J%2Cp%2Ca%2Cb%2C04%2Cm%2C1M" \
                              "%2C08%2C03%2CS%2C0G%2C1Q%2Cq%2C1F%2CL%2C2%2C6%2CY%2CZ%2C1P%2C0M%2C1G%2Cf%2C1%2C07%2C8" \
                              "%2C9%2C1H%2C1I%2CO%2CH%2C0E%2CW%2Cx%2CG%2Co%2C06%2C3%2CR%2Cd%2CQ%2Cn%2Cy%2CT%2Ci%2Cr" \
                              "%2Cu%2Cl%2C4%2CN%2CM%2C01%2C09%2CV%2C7%2C5%2C0H%2Cg%2Cs%2Cc%2CF%2Ct%2C0L%2C0W%2C1N" \
                              "%2C0X%2Ck%2C00%2Cz%2C19%2CK%2C0K%2CE%2C02%2CI%2C1E%2CJ%2Cj%2CD%2Ch%2C1L%2C05%2C1A%2CX" \
                              "%2Cv%2C0e%2Ccom.verizon.hardware.telephony.lte%2Ccom.verizon.hardware.telephony.ehrpd" \
                              "%2Ccom.google.android.feature.D2D_CABLE_MIGRATION_FEATURE%2Candroid.hardware" \
                              ".reboot_escrow%2Ccom.google.android.feature.PIXEL_2017_EXPERIENCE%2Ccom.google.android" \
                              ".feature.PIXEL_2018_EXPERIENCE%2Ccom.google.android.feature.PIXEL_2019_EXPERIENCE" \
                              "%2Ccom.google.android.feature.GOOGLE_BUILD%2Candroid.software.opengles.deqp.level" \
                              "%2Candroid.hardware.sensor.hifi_sensors%2Ccom.google.android.apps.photos" \
                              ".PIXEL_2019_PRELOAD%2Ccom.google.android.feature.TURBO_PRELOAD%2Candroid.hardware" \
                              ".context_hub%2Ccom.google.android.feature.PIXEL_EXPERIENCE%2Ccom.google.android" \
                              ".feature.GOOGLE_FI_BUNDLED%2Candroid.hardware.telephony.carrierlock%2Ccom.google" \
                              ".android.feature.WELLBEING%2Candroid.hardware.device_unique_attestation%2Candroid" \
                              ".software.device_id_attestation%2Ccom.google.android.feature.AER_OPTIMIZED%2Ccom" \
                              ".google.android.feature.NEXT_GENERATION_ASSISTANT%2Ccom.google.android.feature" \
                              ".PIXEL_2019_MIDYEAR_EXPERIENCE%2Ccom.google.android.apps.dialer.SUPPORTED%2Candroid" \
                              ".hardware.identity_credential%2Ccom.google.android.feature.GOOGLE_EXPERIENCE%2Ccom" \
                              ".google.android.feature.EXCHANGE_6_2%2Candroid.hardware.sensor.assist%2Ccom.google" \
                              ".android.feature.DREAMLINER%2Ccom.google.android.feature.ADAPTIVE_CHARGING%22%2C%22dpi" \
                              "%22%3A560%2C%22openglExts%22%3A%221%2C0y%2C1d%2C1e%2C1f%2C0c%2CM%2CO%2C0q%2C0r%2C0s" \
                              "%2CB%2CA%2C5%2C4%2C0p%2CD%2CE%2C0m%2C0n%2C7%2C0i%2C0j%2C0k%2C8%2C0t%2C0w%2C1g%2C1o" \
                              "%2C1m%2C1n%2CH%2C0u%2C1i%2C1l%22%2C%22preferLan%22%3A%22en%22%2C%22usesLibrary%22%3A" \
                              "%225%2C6%2C4%2C2l%2C1H%2CG%2C2m%2C10%2C3%2C09%2C0r%2CA%2C0U%2C9%2C28%2C2%2Cb%2C0Q%2CE" \
                              "%2C0I%2C0J%2C08%2C7%2Cd%2C0V%2CD%2CB%2CC%2C0X%2C0Y%2C0Z%2Ccom.vzw.apnlib%2Ccom.android" \
                              ".hotwordenrollment.common.util%2Cgoogle-ril%2Ccom.android.omadm.radioconfig%2Ccom" \
                              ".qualcomm.qmapbridge%2Clibairbrush-pixel.so%2Ccom.google.android.camera" \
                              ".experimental2019%2ClibOpenCL-pixel.so%2Clib_aion_buffer.so%2ClibqdMetaData.so%2Ccom" \
                              ".google.android.dialer.support%2Ccom.google.android.camera.extensions%2Ccom.google" \
                              ".android.hardwareinfo%2Cqti-telephony-hidl-wrapper-prd%22%7D&fid=0&gaid=2624c0c0-ee52" \
                              "-489b-b6fd-0bf7c06aec4e&globalTrace=null&gradeLevel=0&gradeType=&hardwareType=0" \
                              "&isSupportPage=1&manufacturer=Google&maxResults=25&method=client.getTabDetail&net=1" \
                              "&oaidTrack=1&osv=12&outside=0&recommendSwitch=0&reqPageNum={}&roamingTime=0&runMode=2" \
                              "&serviceType=0&shellApkVer=0&sid=1676915478366&sign" \
                              "=s90035901q0001042000001007u003500a0000000600100000011280000010000050240b0000011000" \
                              "%4008D60505D236459CAA43754B067735DC&thirdPartyPkg=com.huawei.appmarket&translateFlag=1" \
                              "&ts=1676915519479&uri={}&ver=1.1 "

app_details_req_body = "apsid=1676922795932&arkMaxVersion=0&arkMinVersion=0&arkSupport=0&brand=google&channelId" \
                       "=background&clientPackage=com.huawei.appmarket&cno=4010001&code=0200&contentPkg" \
                       "=&dataFilterSwitch=&deviceId=0aa3ba61d395d5f24020f71b56c6e5ef02d1bffd3871016f2f037af24ae10b84" \
                       "&deviceIdRealType=4&deviceIdType=9&deviceSpecParams=%7B%22abis%22%3A%22arm64-v8a%2Carmeabi" \
                       "-v7a%2Carmeabi%22%2C%22deviceFeatures%22%3A%22U%2CP%2C1O%2CB%2C0c%2Ce%2C0J%2Cp%2Ca%2Cb%2C04" \
                       "%2Cm%2C1M%2C08%2C03%2CS%2C0G%2C1Q%2Cq%2C1F%2CL%2C2%2C6%2CY%2CZ%2C1P%2C0M%2C1G%2Cf%2C1%2C07" \
                       "%2C8%2C9%2C1H%2C1I%2CO%2CH%2C0E%2CW%2Cx%2CG%2Co%2C06%2C3%2CR%2Cd%2CQ%2Cn%2Cy%2CT%2Ci%2Cr%2Cu" \
                       "%2Cl%2C4%2CN%2CM%2C01%2C09%2CV%2C7%2C5%2C0H%2Cg%2Cs%2Cc%2CF%2Ct%2C0L%2C0W%2C1N%2C0X%2Ck%2C00" \
                       "%2Cz%2C19%2CK%2C0K%2CE%2C02%2CI%2C1E%2CJ%2Cj%2CD%2Ch%2C1L%2C05%2C1A%2CX%2Cv%2C0e%2Ccom" \
                       ".verizon.hardware.telephony.lte%2Ccom.verizon.hardware.telephony.ehrpd%2Ccom.google.android" \
                       ".feature.D2D_CABLE_MIGRATION_FEATURE%2Candroid.hardware.reboot_escrow%2Ccom.google.android" \
                       ".feature.PIXEL_2017_EXPERIENCE%2Ccom.google.android.feature.PIXEL_2018_EXPERIENCE%2Ccom" \
                       ".google.android.feature.PIXEL_2019_EXPERIENCE%2Ccom.google.android.feature.GOOGLE_BUILD" \
                       "%2Candroid.software.opengles.deqp.level%2Candroid.hardware.sensor.hifi_sensors%2Ccom.google" \
                       ".android.apps.photos.PIXEL_2019_PRELOAD%2Ccom.google.android.feature.TURBO_PRELOAD%2Candroid" \
                       ".hardware.context_hub%2Ccom.google.android.feature.PIXEL_EXPERIENCE%2Ccom.google.android" \
                       ".feature.GOOGLE_FI_BUNDLED%2Candroid.hardware.telephony.carrierlock%2Ccom.google.android" \
                       ".feature.WELLBEING%2Candroid.hardware.device_unique_attestation%2Candroid.software" \
                       ".device_id_attestation%2Ccom.google.android.feature.AER_OPTIMIZED%2Ccom.google.android" \
                       ".feature.NEXT_GENERATION_ASSISTANT%2Ccom.google.android.feature.PIXEL_2019_MIDYEAR_EXPERIENCE" \
                       "%2Ccom.google.android.apps.dialer.SUPPORTED%2Candroid.hardware.identity_credential%2Ccom" \
                       ".google.android.feature.GOOGLE_EXPERIENCE%2Ccom.google.android.feature.EXCHANGE_6_2%2Candroid" \
                       ".hardware.sensor.assist%2Ccom.google.android.feature.DREAMLINER%2Ccom.google.android.feature" \
                       ".ADAPTIVE_CHARGING%22%2C%22dpi%22%3A560%2C%22openglExts%22%3A%221%2C0y%2C1d%2C1e%2C1f%2C0c" \
                       "%2CM%2CO%2C0q%2C0r%2C0s%2CB%2CA%2C5%2C4%2C0p%2CD%2CE%2C0m%2C0n%2C7%2C0i%2C0j%2C0k%2C8%2C0t" \
                       "%2C0w%2C1g%2C1o%2C1m%2C1n%2CH%2C0u%2C1i%2C1l%22%2C%22preferLan%22%3A%22en%22%2C%22usesLibrary" \
                       "%22%3A%225%2C6%2C4%2C2l%2C1H%2CG%2C2m%2C10%2C3%2C09%2C0r%2CA%2C0U%2C9%2C28%2C2%2Cb%2C0Q%2CE" \
                       "%2C0I%2C0J%2C08%2C7%2Cd%2C0V%2CD%2CB%2CC%2C0X%2C0Y%2C0Z%2Ccom.vzw.apnlib%2Ccom.android" \
                       ".hotwordenrollment.common.util%2Cgoogle-ril%2Ccom.android.omadm.radioconfig%2Ccom.qualcomm" \
                       ".qmapbridge%2Clibairbrush-pixel.so%2Ccom.google.android.camera.experimental2019%2ClibOpenCL" \
                       "-pixel.so%2Clib_aion_buffer.so%2ClibqdMetaData.so%2Ccom.google.android.dialer.support%2Ccom" \
                       ".google.android.camera.extensions%2Ccom.google.android.hardwareinfo%2Cqti-telephony-hidl" \
                       "-wrapper-prd%22%7D&fid=0&gaid=2624c0c0-ee52-489b-b6fd-0bf7c06aec4e&globalTrace=null" \
                       "&gradeLevel=0&gradeType=&hardwareType=0&isSupportPage=1&manufacturer=Google&maxResults=25" \
                       "&method=client.getTabDetail&net=1&oaidTrack=1&osv=12&outside=0&recommendSwitch=0&reqPageNum=1" \
                       "&roamingTime=1676922798752&runMode=2&serviceType=0&shellApkVer=0&sid=1676923777736&sign" \
                       "=s90035901q0001042000001007u323200a0000000600100000011280000010000050240b0000011000" \
                       "%407036702ABA594C4099E856206CA30944&thirdPartyPkg=com.huawei.appmarket&translateFlag=1&ts" \
                       "=1676923802607&uri={}&ver=1.1"

game_categories_req_body = "apsid=1676995976030&arkMaxVersion=0&arkMinVersion=0&arkSupport=0&brand=google&channelId" \
                           "=background&clientPackage=com.huawei.appmarket&cno=4010001&code=0200&contentPkg" \
                           "=&dataFilterSwitch=&deviceId" \
                           "=0aa3ba61d395d5f24020f71b56c6e5ef02d1bffd3871016f2f037af24ae10b84&deviceIdRealType=4" \
                           "&deviceIdType=9&deviceSpecParams=%7B%22abis%22%3A%22arm64-v8a%2Carmeabi-v7a%2Carmeabi%22" \
                           "%2C%22deviceFeatures%22%3A%22U%2CP%2C1O%2CB%2C0c%2Ce%2C0J%2Cp%2Ca%2Cb%2C04%2Cm%2C1M%2C08" \
                           "%2C03%2CS%2C0G%2C1Q%2Cq%2C1F%2CL%2C2%2C6%2CY%2CZ%2C1P%2C0M%2C1G%2Cf%2C1%2C07%2C8%2C9%2C1H" \
                           "%2C1I%2CO%2CH%2C0E%2CW%2Cx%2CG%2Co%2C06%2C3%2CR%2Cd%2CQ%2Cn%2Cy%2CT%2Ci%2Cr%2Cu%2Cl%2C4" \
                           "%2CN%2CM%2C01%2C09%2CV%2C7%2C5%2C0H%2Cg%2Cs%2Cc%2CF%2Ct%2C0L%2C0W%2C1N%2C0X%2Ck%2C00%2Cz" \
                           "%2C19%2CK%2C0K%2CE%2C02%2CI%2C1E%2CJ%2Cj%2CD%2Ch%2C1L%2C05%2C1A%2CX%2Cv%2C0e%2Ccom" \
                           ".verizon.hardware.telephony.lte%2Ccom.verizon.hardware.telephony.ehrpd%2Ccom.google" \
                           ".android.feature.D2D_CABLE_MIGRATION_FEATURE%2Candroid.hardware.reboot_escrow%2Ccom" \
                           ".google.android.feature.PIXEL_2017_EXPERIENCE%2Ccom.google.android.feature" \
                           ".PIXEL_2018_EXPERIENCE%2Ccom.google.android.feature.PIXEL_2019_EXPERIENCE%2Ccom.google" \
                           ".android.feature.GOOGLE_BUILD%2Candroid.software.opengles.deqp.level%2Candroid.hardware" \
                           ".sensor.hifi_sensors%2Ccom.google.android.apps.photos.PIXEL_2019_PRELOAD%2Ccom.google" \
                           ".android.feature.TURBO_PRELOAD%2Candroid.hardware.context_hub%2Ccom.google.android" \
                           ".feature.PIXEL_EXPERIENCE%2Ccom.google.android.feature.GOOGLE_FI_BUNDLED%2Candroid" \
                           ".hardware.telephony.carrierlock%2Ccom.google.android.feature.WELLBEING%2Candroid.hardware" \
                           ".device_unique_attestation%2Candroid.software.device_id_attestation%2Ccom.google.android" \
                           ".feature.AER_OPTIMIZED%2Ccom.google.android.feature.NEXT_GENERATION_ASSISTANT%2Ccom" \
                           ".google.android.feature.PIXEL_2019_MIDYEAR_EXPERIENCE%2Ccom.google.android.apps.dialer" \
                           ".SUPPORTED%2Candroid.hardware.identity_credential%2Ccom.google.android.feature" \
                           ".GOOGLE_EXPERIENCE%2Ccom.google.android.feature.EXCHANGE_6_2%2Candroid.hardware.sensor" \
                           ".assist%2Ccom.google.android.feature.DREAMLINER%2Ccom.google.android.feature" \
                           ".ADAPTIVE_CHARGING%22%2C%22dpi%22%3A560%2C%22openglExts%22%3A%221%2C0y%2C1d%2C1e%2C1f" \
                           "%2C0c%2CM%2CO%2C0q%2C0r%2C0s%2CB%2CA%2C5%2C4%2C0p%2CD%2CE%2C0m%2C0n%2C7%2C0i%2C0j%2C0k" \
                           "%2C8%2C0t%2C0w%2C1g%2C1o%2C1m%2C1n%2CH%2C0u%2C1i%2C1l%22%2C%22preferLan%22%3A%22en%22%2C" \
                           "%22usesLibrary%22%3A%225%2C6%2C4%2C2l%2C1H%2CG%2C2m%2C10%2C3%2C09%2C0r%2CA%2C0U%2C9%2C28" \
                           "%2C2%2Cb%2C0Q%2CE%2C0I%2C0J%2C08%2C7%2Cd%2C0V%2CD%2CB%2CC%2C0X%2C0Y%2C0Z%2Ccom.vzw.apnlib" \
                           "%2Ccom.android.hotwordenrollment.common.util%2Cgoogle-ril%2Ccom.android.omadm.radioconfig" \
                           "%2Ccom.qualcomm.qmapbridge%2Clibairbrush-pixel.so%2Ccom.google.android.camera" \
                           ".experimental2019%2ClibOpenCL-pixel.so%2Clib_aion_buffer.so%2ClibqdMetaData.so%2Ccom" \
                           ".google.android.dialer.support%2Ccom.google.android.camera.extensions%2Ccom.google" \
                           ".android.hardwareinfo%2Cqti-telephony-hidl-wrapper-prd%22%7D&fid=0&gaid=2624c0c0-ee52" \
                           "-489b-b6fd-0bf7c06aec4e&globalTrace=null&gradeLevel=0&gradeType=&hardwareType=0" \
                           "&isSupportPage=1&manufacturer=Google&maxResults=25&method=client.getTabDetail&net=1" \
                           "&oaidTrack=1&osv=12&outside=0&recommendSwitch=0&reqPageNum=4&roamingTime=1676922798752" \
                           "&runMode=2&serviceType=0&shellApkVer=0&sid=1676996016763&sign" \
                           "=s90035901q0001042000001007u323200a0000000600100000011280000010000050240b0000011000" \
                           "%40629A627603A1410796FAF54BE4938D6E&thirdPartyPkg=com.huawei.appmarket&translateFlag=0&ts" \
                           "=1676996019562&uri=0302009f16254ba6ae6608aa6d88a031%3Faglocation%3D%257B%2522cres%2522" \
                           "%253A%257B%2522lPos%2522%253A0%252C%2522pos%2522%253A3%252C%2522resid%2522%253A" \
                           "%25220302009f16254ba6ae6608aa6d88a031%2522%252C%2522rest%2522%253A%2522tab%2522%252C" \
                           "%2522tid%2522%253A%2522dist_0302009f16254ba6ae6608aa6d88a031%2522%257D%252C%2522ftid%2522" \
                           "%253A%2522dist_0302009f16254ba6ae6608aa6d88a031%2522%257D%26templateId" \
                           "%3D871221ec262b45b89011bb154fb9af46&ver=1.1 "


async def get_category_content(session, category, file):
    page = 1
    finished = False

    while not finished:
        print("Getting category contents from: {}".format(base_appgallery_url))
        async with session.post(base_appgallery_url,
                                data=categories_content_req_body.format(page, category['detailId']),
                                verify_ssl=True) as response:

            response_json = await response.json()
            apps = response_json['layoutData'][0]['dataList']

            for app in apps:
                await get_app_details(session, app, category, file)

            if response_json['hasNextPage'] == 1:
                page += 1
            else:
                finished = True


async def get_app_details(session, app, category, file):
    async with session.post(base_appgallery_url,
                            data=app_details_req_body.format(app['detailId']),
                            verify_ssl=True) as response:
        print("Getting app details from {}".format(base_appgallery_url))
        app_details = await response.json()
        res_app = dict()
        app_info_block = dict()
        app_developer_block = dict()
        app_metrics_block = dict()

        for layoutData in app_details['layoutData']:
            try:
                if layoutData['dataList'][0]['name'] is not None:
                    app_info_block = layoutData['dataList'][0]
                    break
            except:
                continue

        for layoutData in app_details['layoutData']:
            try:
                if layoutData['dataList'][0]['developer'] is not None:
                    app_developer_block = layoutData['dataList'][0]
                    break
            except:
                continue

        for layoutData in app_details['layoutData']:
            try:
                if layoutData['dataList'][0]['score'] is not None:
                    app_metrics_block = layoutData['dataList'][0]
                    break
            except:
                continue

        res_app['category'] = category['name']
        res_app['packageName'] = app_info_block['package']
        res_app['versionName'] = app_info_block['versionName']
        res_app['versionCode'] = app_info_block['versionCode']
        res_app['name'] = app_info_block['name']
        try:
            res_app['company'] = app_developer_block['developer']
        except:
            res_app['company'] = ""
        res_app['rating'] = app_metrics_block['score']
        res_app['downloads'] = app_metrics_block['downloads']

        await write_to_csv(file, res_app)


def get_categories():
    result = []
    apps_categories_response = requests.post(base_appgallery_url, data=categories_req_body, verify=True)
    print("Getting application categories from {}".format(base_appgallery_url))
    result.extend(json.loads(apps_categories_response.text)['layoutData'][0]['dataList'])
    games_categories_response = requests.post(base_appgallery_url, data=game_categories_req_body, verify=True)
    print("Getting application game categories from {}".format(base_appgallery_url))
    result.extend(json.loads(games_categories_response.text)['layoutData'][2]['dataList'])
    return result


async def open_csv(file):
    writer = AsyncWriter(file)
    await writer.writerow(
        #['ID', 'Name', 'Category', 'Company name', 'Version name', 'Version code', 'Installs', 'Rating']
        ['ID', 'Version name', 'Version code']
    )


async def write_to_csv(file, app):
    print("Writing results to appgallery_dump.csv")
    writer = AsyncWriter(file)
    await writer.writerow(
        [
            app['packageName'],
            #app['name'],
            #app['category'],
            #app['company'],
            app['versionName'],
            app['versionCode'],
            #app['downloads'],
            #app['rating'] if app['rating'] is not None else 0
        ]
    )


async def main():
    categories = get_categories()
    print(categories)
    async with aiofiles.open('appgallery_dump.csv', 'w', encoding="utf-8") as file:
        await open_csv(file)
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=True)) as session:
            categoriesCoroutines = [get_category_content(session, category, file) for category in categories]
            await asyncio.gather(*categoriesCoroutines)
            print("Finished")


if __name__ == '__main__':
    asyncio.run(main())
