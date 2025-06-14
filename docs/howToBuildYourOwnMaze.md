# Maze Construction

This tutorial describes how we built our autoamted maze in the [Niell Lab](https://nielllab.uoregon.edu/).

***Important: this tutorial is currently under development***

<p align="center">
<img width="500" height="300" src="../assets/mazeTopView.png">
<img width="500" height="300" src="../assets/mazeComponents.png">
</p>

# Components

## Maze

1. 1" T-slotted [squared](https://www.mcmaster.com/47065T101/) and [rounded](https://www.mcmaster.com/3136N27/) framing rails, cut to a custom size with 1/4"-20 threads on both ends.
2. Sign white 9 % light transmission [acrylic](https://www.tapplastics.com/product/plastics/cut_to_size_plastic/acrylic_sheets_color/341) for the floor, walls and doors of the maze.
3. 1" [brakets](https://www.mcmaster.com/47065T236/) and [cubes](https://www.mcmaster.com/47065T244/) to assemble the structural frame of the maze.
4. A white melamine [wood shelf](https://www.homedepot.com/p/White-Melamine-Wood-Shelf-23-75-in-D-x-48-in-L-252297/202089063) with 2" [caster wheels](https://www.amazon.com/Casters-Locking-Castors-Furniture-Kitchen/dp/B09QZMTSCQ/ref=pd_bxgy_img_d_sccl_2/142-9516444-0421340?pd_rd_w=h5m3x&content-id=amzn1.sym.839d7715-b862-4989-8f65-c6f9502d15f9&pf_rd_p=839d7715-b862-4989-8f65-c6f9502d15f9&pf_rd_r=FRMHFY3ZBWA5QW7X6ASM&pd_rd_wg=8v5Oh&pd_rd_r=5618abc9-7d00-4d7a-a696-668fa49b88b9&pd_rd_i=B0BFXLTQNH&th=1) for the base of the maze.
5. A 10" [screen](https://www.amazon.com/dp/B0987468N2/ref=sspa_dk_detail_4?pd_rd_i=B0987468N2&pd_rd_w=QqC5K&content-id=amzn1.sym.386c274b-4bfe-4421-9052-a1a56db557ab&pf_rd_p=386c274b-4bfe-4421-9052-a1a56db557ab&pf_rd_r=1QH3Q0EH5X5P3PGTJ3EK&pd_rd_wg=wrki0&pd_rd_r=280cd8b9-b4b4-4a81-84ca-9a71bb273634&s=pc&sp_csd=d2lkZ2V0TmFtZT1zcF9kZXRhaWxfdGhlbWF0aWM&th=1) for displaying visual stimuli.
6. Mini USB [speaker](https://www.adafruit.com/product/3369?gclid=Cj0KCQjw9fqnBhDSARIsAHlcQYQN7-PUcKRt7g5K4LZLOxeUrOmGBO-mkdPEippvQnJ8RdAV6c8ZS8oaAvPWEALw_wcB) for signaling correct and incorrect trials.
7. Diffused 5 mm [LEDs](https://www.adafruit.com/product/4203?gclid=Cj0KCQjw9fqnBhDSARIsAHlcQYQOVymyhPb8JML-s9yA5havhJG0yBzvc3udh55acPwMJ-_8xEU4wKcaAnpeEALw_wcB) for signaling correct trials.
8. [Solenoid valves](https://www.theleeco.com/industries/scientific-instruments/products/solenoid-valves/browse/?filters[subtype][]=Control+Solenoid+Valves) for control of water delivery.
9. 1/16" ID x 1/8" OD Tygon [tubing](https://www.usplastic.com/catalog/item.aspx?itemid=91104&catid=864) for the water delivery system.
10. 14 gauge luer-lock blunt tip [needles](https://www.amazon.com/Syringe-Dispensing-Needles-Length-Interface/dp/B07DZC225B/ref=pd_ci_mcx_di_int_sccai_cn_d_sccl_2_1/133-0408013-9182656?pd_rd_w=JuARf&content-id=amzn1.sym.751acc83-5c05-42d0-a15e-303622651e1e&pf_rd_p=751acc83-5c05-42d0-a15e-303622651e1e&pf_rd_r=SDJGVFYGQZ0KS2EZG109&pd_rd_wg=XP1nb&pd_rd_r=9ea53b80-e963-4a30-bfc5-857ae6b058f9&pd_rd_i=B07DZC225B&psc=1) as spouts for water delivery.
11. Custom [3D-printed objects](https://github.com/luismfranco/automatedMouseMaze/tree/99c225861e82ac3776c7e1dc496d73c4fc0f3bcc/assets/hardware) as rail brakets, sections of walls (i.e., water ports, stimulus screen holders), and to mount other components (i.e., IR sensors, speaker, cables, water system).
12. A blackout [curtain](https://evertrack.co/blackout-room-divider-curtain-eclipse-satin/?utm_term=&utm_campaign=PMAX+-+Room+Divider+Curtains&utm_source=adwords&utm_medium=ppc&hsa_acc=5806130293&hsa_cam=22123857351&hsa_grp=&hsa_ad=&hsa_src=x&hsa_tgt=&hsa_kw=&hsa_mt=&hsa_net=adwords&hsa_ver=3&gad_source=1&gclid=Cj0KCQjw4v6-BhDuARIsALprm32yAWsM92bhXs5Hm0Y3QMyoQlhOliOSD0VcVHp_9gU-yHXiStgtKXEaAvcoEALw_wcB) and [rail](https://www.amazon.com/dp/B0C69LGQW1/ref=sspa_dk_detail_2?pd_rd_i=B0C69LGQW1&pd_rd_w=YEFyC&content-id=amzn1.sym.386c274b-4bfe-4421-9052-a1a56db557ab&pf_rd_p=386c274b-4bfe-4421-9052-a1a56db557ab&pf_rd_r=B9N6694BX21GFFRSVHP6&pd_rd_wg=QsIWq&pd_rd_r=c0aed70f-5ff7-4f5d-a2dd-321a2899c61f&s=kitchen&sp_csd=d2lkZ2V0TmFtZT1zcF9kZXRhaWxfdGhlbWF0aWM&th=1) to isolate the maze and mice from external distractions.

## Automated Doors

1. [Pneumatic actuators](https://www.amazon.com/Baomain-Pneumatic-Cylinder-SC-Screwed/dp/B01F9XZQ1K/ref=pd_ci_mcx_di_int_sccai_cn_d_sccl_2_2/136-8001444-7379768?pd_rd_w=CoJWI&content-id=amzn1.sym.751acc83-5c05-42d0-a15e-303622651e1e&pf_rd_p=751acc83-5c05-42d0-a15e-303622651e1e&pf_rd_r=AXNT0SNVR13YJT89ZTJJ&pd_rd_wg=F8NEU&pd_rd_r=9dcf470c-de43-4689-a980-ca5e8e994869&pd_rd_i=B01F9XZQ1K&th=1) for movement of the automated doors.
2. A [solenoid manifold](https://www.amazon.com/Baomain-4V210-08-Position-Pneumatic-Solenoid/dp/B01D9IGCTC/ref=sims_dp_d_dex_ai_speed_loc_mtl_v4_d_sccl_4_1/136-8001444-7379768?pd_rd_w=QAJm3&content-id=amzn1.sym.af515e1d-64ab-47a5-8a2e-6be4d0f4cdc5&pf_rd_p=af515e1d-64ab-47a5-8a2e-6be4d0f4cdc5&pf_rd_r=QQ6ZJF00XSNFZP6H8B3Z&pd_rd_wg=ip6Yj&pd_rd_r=6282a60c-3df6-4d58-8258-af29a286d7ae&pd_rd_i=B01D9IGCTC&psc=1) for controlling the automated doors.
3. [6 mm](https://www.amazon.com/Tailonz-Pneumatic-Black-Polyurethane-32-8ft/dp/B08GC6TR2S/ref=sr_1_6?crid=B4SJCL6S8C9C&dib=eyJ2IjoiMSJ9.DejGkL7N9ogqAzdCGOySW8Ul4oFXYI6uTvpMsLFLQavsPcgyc9dCZSS0RZEDuOVTGBNc74dp5AgyndprPP87Hf5uJyTtiH9rcP7fQU8OTkzCA8K8Lv6_3velU18rnE5GaAfLZ6q1gyariRIkULl7URyfKc2KDw0pVo_LMPqGbvt8MmwsfXPHnCfzkYaMb4eLXCrkmvK0VoPedBBdU368PWvUj1i6hELtX5D_il5MeDzO23k3WryqV_aB2wbEvVOaP6Nks4V_xsxegeLF3uYnt_uTJ9Vwoqsxe3ukTBuhLVI.ajZ5AaE_mu1l8TI9caTWLeYIIOOZVvQAvAvGWvogzXg&dib_tag=se&keywords=Air%2BLine%2BTubing%2BKit%2B6mm%2Bblack&qid=1714772204&s=industrial&sprefix=air%2Bline%2Btubing%2Bkit%2B6mm%2Bblac%2Cindustrial%2C121&sr=1-6&th=1) and [8 mm](https://www.amazon.com/CGELE-Pneumatic-Transfer-OD-39-4Ft-12Meter/dp/B09LS1S7MK/ref=sr_1_3?crid=1UCLWG8RC00F5&dib=eyJ2IjoiMSJ9.9IT0mdNrbcPPwFnwS3lttd1-X4Lt2TRh2Ekuy9jjREetTrO9R6abyOPbWKJOIBw0.COukHekBEaDTeMd4yj45MHDLXDYYBJPRxJqthZbJgoc&dib_tag=se&keywords=TAILONZ%2BPNEUMATIC%2BBlack%2B5%2F16&qid=1724450805&s=hi&sprefix=tailonz%2Bpneumatic%2Bblack%2B5%2F1%2Ctools%2C144&sr=1-3&th=1) tubing for air connections, as well as [adapters](https://www.amazon.com/Metalwork-Straight-Reducing-Pneumatic-Connector/dp/B07C7BGQ9S/ref=sr_1_5?crid=2EOM3OXEO5504&dib=eyJ2IjoiMSJ9.sZVireplGplt2H6sWKEogbyxddOqDaPAou-Hecj9GtV1WioAia-WJQIGtxOWdVFVTQup_Kqhm3tuUmI4i797ggSqxKtK6BQcITqGEm_J8Jd80-lc9OO1TKfBGQq-wL9LLAby1xOZYYVYpjkhlgDVuNfve2of7sbq0TFmEraXme2kNnz8YlwITV7zWLn_CfpviRaNwQc0ZqtmgVXMZVcHYADlHSF5U06SYpBPrxmvLaM.iJ10JiNAwGi4COcf2CwCBSLYdg1aO_1qU6pIi8fo8Nk&dib_tag=se&keywords=10%2Bmm%2Bto%2B6%2Bmm%2Bair%2Btubing%2Badapter&qid=1724450958&sprefix=10%2Bmm%2Bto%2B6%2Bmm%2Bair%2Btubing%2Badapter%2Caps%2C214&sr=8-5&th=1).
4. Air flow [control valves](https://www.amazon.com/dp/B0BMFV48YB/ref=sspa_dk_detail_1?pd_rd_i=B0BMFSYB5Q&pd_rd_w=VSRTa&content-id=amzn1.sym.8c2f9165-8e93-42a1-8313-73d3809141a2&pf_rd_p=8c2f9165-8e93-42a1-8313-73d3809141a2&pf_rd_r=2GSZVHJ84JHSYXGXWF79&pd_rd_wg=rD2xV&pd_rd_r=86c33250-2e60-44ee-addf-e33c132e3863&s=hi&sp_csd=d2lkZ2V0TmFtZT1zcF9kZXRhaWw&th=1) for controlling the speed of the doors.
5. A [regulator](https://www.amazon.com/dp/B09MLMFF2K/ref=sspa_dk_detail_4?pd_rd_i=B09MLMFF2K&pd_rd_w=U3UuV&content-id=amzn1.sym.8c2f9165-8e93-42a1-8313-73d3809141a2&pf_rd_p=8c2f9165-8e93-42a1-8313-73d3809141a2&pf_rd_r=DGYB1C9ZMZ9F3ED5QBE2&pd_rd_wg=BIhvv&pd_rd_r=dd296391-c469-481f-a3ac-71e60c75697b&s=industrial&sp_csd=d2lkZ2V0TmFtZT1zcF9kZXRhaWw&th=1) for setting the input air pressure to the solenoid manifold.
6. IR [beam breaks](https://www.adafruit.com/product/2167) for detecting the mouse traverse through the maze.
7. 100 cm M/M [wires](https://www.amazon.com/EDGELEC-Breadboard-Optional-Assorted-Multicolored/dp/B07GD1W7XV/ref=sr_1_1_sspa?crid=1D6I1EZM32X2T&dib=eyJ2IjoiMSJ9.tjHxIQLJsk16_0YVtUGN6YeXdt0VqIwh7Zmfzd7nvfTaoSMecktPIPsgfi6eLwfPrpE-Z7TFF3Gb6OmAsEyH4OuRfeKQ2U6yeUaDnbuFGswrOXPukg3xDJGZqP0xiogOAQo_2PqBlSW5yXpFgDqxkBzMUHsNNzfc4F-zrGIxkpvzX6CnOzBpjidBHCxZRSphsHbICibgDRfXkQytRIVXbw9Gbyz2Bt6wmlDkohLT7gUYbs8jQcpc5IITMBIXfrioVjBJ50nB4BJkOvXv_kzaIx5H3ulgZPomOofbuDLn7Cw.BAJcuUxcOIL5un-H80QwuIrBCIlUhJ-gg4DElPhICeA&dib_tag=se&keywords=jumper%2Bwires&qid=1718926518&s=industrial&sprefix=jumper%2Bwire%2Cindustrial%2C148&sr=1-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1) and 1" F/F [wires](https://www.digikey.com/en/products/detail/pololu-corporation/3860/10451018) for connections between IR sensors, water valves and LEDs to the Teensy circuit.
8. 12" M/M [wires](https://www.digikey.com/en/products/detail/pololu-corporation/1765/10450795) and 2" M/F [wires](https://www.digikey.com/en/products/detail/pololu-corporation/3845/10451009) for connections between the solenoid manifold and the Teensy circuit.
9. Custom [3D-printed objects](https://github.com/luismfranco/automatedMouseMaze/tree/99c225861e82ac3776c7e1dc496d73c4fc0f3bcc/assets/hardware) to mount the pneumatic actuators, to cushion and limit the range of motion of actuators, and to secure the acrylic doors to the actuators.
10. Foam [cushioning](https://www.amazon.com/Adhesive-Neoprene-Insulation-Furniture-Speakers/dp/B0CRQXWQVW/ref=sr_1_31?crid=1WAQENVGHAASI&dib=eyJ2IjoiMSJ9.xDBOrBm9YUYY52LlaKfoQZn7treA9NnboDS11bCZ1cS9WmyQNHZTXRrBV4mlwpaAVph5KWOLrZbCAz2k90Mw6IzJ3utfqgWq1d8K4ecApASypii6IHid7ceR9PI5BXThcq9WOmjDtjo4oupGnWj-pRGjheNhrXRMeZC-p__gf4SVxP2Ux_uf0FCsYi_BwsTJSVMe0bS4_WVuybONPMA-5H3so1UD-ifczPZHejo4v5QF1G60yC5xKDJBZKmKJecARzT7cGBr_sFQvAXn8t14im2XqmQXeDD8HagM82Hahu7wz5YRcz7_7jkRdiW9zGMuDFSm3ZyhervMte6CfHMUtMaYyjSsXuQKA8THTfEcsoVsjId5ZDDMHxb-q56tKma9OloKk3uxEIa89kH3iP9oPkKtxbOWncpXTuoaDst85lRNTO9hJL9YGzMSj0idDu_W.fZk5Qenglkk0ea6LycULhD6u9rnjPPaIzF6gw3f70w0&dib_tag=se&keywords=black%2Bfoam%2Bcushion%2Bpads%2Bwith%2Bglue&qid=1734548418&sprefix=black%2Bfoam%2Bcushion%2Bpads%2Bwith%2Bglu%2Caps%2C205&sr=8-31&th=1) for buffering the contact between 3D-printed objects that limit the range of motion of doors.

<p align="center">
<img width="225" height="500" src="../assets/closedMazeDoor.png">
<img width="225" height="500" src="../assets/openMazeDoor.png">
</p>

## Teensy Circuit

1. [Teensy 4.0](https://www.sparkfun.com/teensy-4-0-headers.html) for processing inputs and outputs between the computer and the different components in the maze.
2. [Bread board](https://www.digikey.com/en/products/detail/sparkfun-electronics/PRT-12699/5762439?utm_adgroup=&utm_source=google&utm_medium=cpc&utm_campaign=PMax%20Shopping_Product_High%20ROAS%20Categories&utm_term=&utm_content=&utm_id=go_cmp-20222717502_adg-_ad-__dev-c_ext-_prd-5762439_sig-CjwKCAjwr7ayBhAPEiwA6EIGxH0-nJ1QtJauifHs8d_4uKSnMKyhCQBnSeDmUdDhgQHYUU73eKNs0RoCaYkQAvD_BwE&gad_source=1&gclid=CjwKCAjwr7ayBhAPEiwA6EIGxH0-nJ1QtJauifHs8d_4uKSnMKyhCQBnSeDmUdDhgQHYUU73eKNs0RoCaYkQAvD_BwE) for building the circuit.
3. NPN [transistors](https://www.digikey.com/en/products/detail/onsemi/BC547B/976366?gclsrc=aw.ds&&utm_adgroup=&utm_source=google&utm_medium=cpc&utm_campaign=PMax%20Shopping_Product_Medium%20ROAS%20Categories&utm_term=&utm_content=&utm_id=go_cmp-20223376311_adg-_ad-__dev-c_ext-_prd-976366_sig-Cj0KCQjwna6_BhCbARIsALId2Z3kIKITUhCn-wMSlmMyu4jYOpSJW8IkK0eGusF3LZLZWlHe61VJmvIaArZBEALw_wcB&gad_source=1&gbraid=0AAAAADrbLlj3So7FqTBK4QOOqqITi_jpy&gclid=Cj0KCQjwna6_BhCbARIsALId2Z3kIKITUhCn-wMSlmMyu4jYOpSJW8IkK0eGusF3LZLZWlHe61VJmvIaArZBEALw_wcB&gclsrc=aw.ds) for control of door and water solenoids with digital outputs from Teensy.
4. [Diodes](https://www.sparkfun.com/diode-rectifier-1a-50v-1n4001.html) to prevent current from flowing back from solenoids to Teensy.
5. 1k Ohm [resistors](https://www.digikey.com/en/products/detail/stackpole-electronics-inc/CFM12JT1K00/1741880) for connections related to IR sensors.
6. 470 Ohm [resistors](https://www.digikey.com/en/products/detail/stackpole-electronics-inc/CF12JT470R/1741161) for connections realted to LEDs.
7. DC barrel jack [adapters](https://www.sparkfun.com/dc-barrel-jack-adapter-breadboard-compatible.html) for power supplies.
8. Assortment of colored [wire](https://www.sparkfun.com/hook-up-wire-assortment-stranded-22-awg.html) for connections.
9. Male and female [header connector kit](https://www.amazon.com/CHENBO-Connector-Housing-Assortment-Terminal/dp/B077X8XV2J/ref=sr_1_3?crid=Q1JQUBJIDW2O&dib=eyJ2IjoiMSJ9.ZV2pcL1tMHr0QntbhCHwV0ABU5A0mO3nzz47YRlN1eukhLKB1KxTg8RLTuKVY2cefXChdFoeeb7-4qEj51dvMKE3YwFLubVw2tVE5V5mKI5Rnvfs7TqBpaU-LIe5K0sfLtOC9KKVJRpxwX8DMGMZNSJDl2xIWvrinbx7aY6gMauFsSAPul0We2oQ65NwJ0giePg-5pNnkUxcWd9oh_RrROWeuBsc72ncFTaPUaNZkijSYoSENe4T6DaoGCXwT9gku17PwkHN8YW9zMFORjBKg9E5ypYWmotWMOTkTOs-0Cg.8VBFpZfhv8JGrCEvoCuEk7HqIESu8TfOJUPnR4w7cag&dib_tag=se&keywords=connector+adapter+for+pin+header&qid=1718053318&s=industrial&sprefix=connector+adapter+for+pin+heade%2Cindustrial%2C111&sr=1-3) for making connections between the Teensy circuit and external wires.
10. 24 V wall adapter [power supply](https://www.amazon.com/gp/product/B095VWHPCC/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&th=1) for the door solenoid manifold.
11. 12 V wall adapter [power supply](https://www.sparkfun.com/wall-adapter-power-supply-12vdc-600ma-barrel-jack.html) for water valves.
12. [Push buttons](https://www.adafruit.com/product/558) for controlling water valves manually.

<p align="center">
<img width="800" height="275" src="../assets/circuitTopView.png">
</p>

## Mouse Cameras and Inertial Measurement Unit (IMU)

1. [Video capture devices](https://www.amazon.com/StarTech-com-USB3HDCAP-Video-Capture-Device/dp/B00PC5HUA6/ref=sr_1_3?crid=1AFS4ZNT5DLU3&dib=eyJ2IjoiMSJ9.2LWQRFf16ZPMxyykpqUm1QtyUSt6AnmngN9oj-gAVxMcaWOHj-sg9mHyR_VOyZlGUHDAgP-RiLVpqHIJ-4CsqHQrcvttvKUw0d4jl_iBUglC5TElRCm2L9J60tKoq5Ut_k4KGTKNtWHq8QpZT8mpwddy7JufOzukyDw1aMnpO24DBLibw6otOFhMhWo_Zq9ubgKt0tLhXP5yMT88ZsZAhWJNJHszQvsijkaGipRK1V4.3MNmDwkGFHCEMfpO7wPUEYZ5Zc35iEvtZ5vzg5dQjI0&dib_tag=se&keywords=startech+usb+3.0+hd+video+capture+device+1080p&qid=1743533019&sprefix=startech+usb+3.0+hd+video+capture+device+1080p%2Caps%2C130&sr=8-3) for converting analog video from both the eye and the world cameras into digital video.
2. An analog 5 mm x 5 mm x 3.6 mm [camera](https://www.aliexpress.us/item/3256803738909660.html?spm=a2g0o.detail.pcDetailTopMoreOtherSeller.10.47a4Gmv2Gmv2Vk&gps-id=pcDetailTopMoreOtherSeller&scm=1007.40196.422467.0&scm_id=1007.40196.422467.0&scm-url=1007.40196.422467.0&pvid=40156854-8944-49dc-8f22-28e36af707d0&_t=gps-id:pcDetailTopMoreOtherSeller,scm-url:1007.40196.422467.0,pvid:40156854-8944-49dc-8f22-28e36af707d0,tpp_buckets:668%232846%238108%231977&pdp_ext_f=%7B%22order%22%3A%2273%22%2C%22eval%22%3A%221%22%2C%22sceneId%22%3A%2230050%22%7D&pdp_npi=4%40dis%21USD%2117.62%2110.12%21%21%2117.62%2110.12%21%402101c5b217435439061578444e0ef5%2112000027485322782%21rec%21US%21%21ABXZ&utparam-url=scene%3ApcDetailTopMoreOtherSeller%7Cquery_from%3A) for recoridng the eye of the mouse.
3. An analog 11 mm x 14.1 mm x 13.5 mm [camera](https://www.amazon.com/BETAFPV-Camera-Sensor-1200TVL-Global/dp/B0BMVFGHB1/ref=asc_df_B0BMVFGHB1?mcid=da343b1b22f63402b7daf4ad020d87c1&hvocijid=17462633199980442399-B0BMVFGHB1-&hvexpln=73&tag=hyprod-20&linkCode=df0&hvadid=721245378154&hvpos=&hvnetw=g&hvrand=17462633199980442399&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9189768&hvtargid=pla-2281435177658&psc=1) for recording the *world* in front of the mouse head.
4. TDK InvenSense [inertial measurement unit](https://invensense.tdk.com/products/motion-tracking/9-axis/icm-20948/) for measuring the position of the head of the mouse.
5. Intan Technologies RHD 6 ft ultra thin SPI [cable](https://intantech.com/RHD_SPI_cables.html?tabSelect=RHDSPIcables) for video and IMU data.
6. A custom-made **crown** to assemble both cameras and the IMU:
   <p align="center">
   <img width="300" height="385" src="../assets/crownLeftSide.png">
   <img width="300" height="385" src="../assets/crownRightSide.png">
   </p>
7. A custom-made breakout board to send video and IMU data from the **crown** to the video capture devices, and to a custom head motion tracking device, respectively:
   <p align="center">
   <img width="430" height="300" src="../assets/crownBreakoutBoard.png">
   </p>
8. A custom head motion tracking device, that uses an [Arduino Nano](https://www.digikey.com/en/products/detail/arduino/A000005/2638989?gclsrc=aw.ds&&utm_adgroup=&utm_source=google&utm_medium=cpc&utm_campaign=PMax%20Shopping_Product_Low%20ROAS%20Categories&utm_term=&utm_content=&utm_id=go_cmp-20243063506_adg-_ad-__dev-c_ext-_prd-2638989_sig-Cj0KCQjw_JzABhC2ARIsAPe3ynqEVYD-BFVXE8fA5tr5GG1G9iT6tvCJUC13k_Zf8-BZ9pDcu-J1IRoaAi5cEALw_wcB&gad_source=1&gbraid=0AAAAADrbLljSkpDyIa89TUOGUGG77v6sQ&gclid=Cj0KCQjw_JzABhC2ARIsAPe3ynqEVYD-BFVXE8fA5tr5GG1G9iT6tvCJUC13k_Zf8-BZ9pDcu-J1IRoaAi5cEALw_wcB&gclsrc=aw.ds) board to read data from the IMU, and send them to the Open Ephys I/O board.
   <p align="center">
   <img width="430" height="300" src="../assets/HMTdeviceFrontView.png">
   <img width="430" height="300" src="../assets/HMTdeviceCircuit.png">
   </p>

## Electrophysiology

1. Open Ephys [acquisition board](https://open-ephys.org/acquisition-system/oeps-9029).
2. Open Ephys [I/O Board](https://open-ephys.org/acquisition-system/io-board-pcb), with through-hole vertical female [BNC connectors](https://www.peconnectors.com/coaxial-rf-connectors-bnc-f-rca/hws3912/?srsltid=AfmBOoo6W5EEuw7a9Wj3TCphOwvCRphM8mKeDhZolUMiHQv2XTFZ-yY3QIs&gQT=1) and a surface-mount [HDMI connector](https://www.digikey.com/en/products/detail/amphenol-cs-fci/10029449-111RLF/2785386?s=N4IgTCBcDaIGwAYCcBaALHAjGlmUDkAREAXQF8g) for connection between the custom head motion tracking device and the Open Ephys acquisition board.
3. A male DB15 to terminal breakout board [connector](https://www.amazon.com/DB15-Breakout-Connector-Pin-Male/dp/B073RGHNVD) for connections between single pins in the D-Sub connector to the Open Ephys I/O board. This is how we connected the DB15 pins to the I/O board, and their correspondance to the IMU data pins through the custom head motion tracking device:

<div align = "center">

   | I/O board hole | DB15 pin | IMU pin |
   | :---: | :---: | :---: |
   | gnd | 8 | GND |
   | 1 | 4 | ACC_X |
   | 2 | 12 | ACC_Y |
   | 3 | 5 | ACC_Z |
   | 5 | 13 | GYRO_X |
   | 6 | 6 | GYRO_Y |
   | 7 | 14 | GYRO_Z |

</div>

<p align="center">
<img width="430" height="325" src="../assets/DB15connectorWithIOboard.png">
</p>


4. A male to female DB15 [cable](https://www.amazon.com/Female-Extension-tinned-Shielded-soliConnector/dp/B093P4W22V/ref=sr_1_5?crid=130GIODUV9ZMD&dib=eyJ2IjoiMSJ9.8Dfuw8gbwaj0Ltt9hNVz6aKSq_yqtXQj2jlV4QmFc4y4sT0Htf3cpZzMWrKl_7DuRt3OoqQtyYHA00QE4swo7XOP6aDjIESvzWZJz_AbNq9HKS9-otb72Ef0sy9F2O8FNDBNScFXaFDjZ9bGLp1yK329s55HWbS-tm0ppJejqisqmffPmw2CRpsBq8liHvQWkC3pBj9iQ86vSZMEVUKZuIpHASC8Zus6WETTaYYXqhI.G9BbIbfxLHvFTva8zR1PQ_lCHkEM7KjyQC1bDxgmQvE&dib_tag=se&keywords=db15%2Bcable%2Bmale%2Bto%2Bfemale%2B3%2Bft&qid=1742251738&sprefix=db15%2Bcable%2Bmale%2Bto%2Bfemale%2B3%2Bft%2Caps%2C152&sr=8-5&th=1) to connect the custom head motion tracking device to the Open Ephys I/O board.
5. An [HDMI cable](https://www.amazon.com/8K-HDMI-Cable-Highwings-Braided/dp/B08NX5CZTF/ref=sr_1_3?crid=2SKNV3K7FT856&dib=eyJ2IjoiMSJ9.0s7nNXqA8Cyls4m55p6IICY9LFpXeLHEcHy1I_FPqAV92uDbZ6TIhbl41YOCkCFidSRUzabDXBDrvh4pv0ZoePQDTtZaBJQwBT6txrHYD13xFO7OUg2KzzUmhyB9yriOJ4LIp5eHkThv963hRvpSOWb0zHB9D1R0EtGbtDyiY9zcurTbybNtn6B363BnccMLb0wQFV-ME9-Ql8XH9SsLLeq9nGqnEYX7qHf7zJj3Bog.j3JsmHsvfzkTRXN6iaeko4XzVftNXnVeqkv6F7fscjs&dib_tag=se&keywords=hdmi%2Bcable&qid=1742258716&sprefix=hdmi%2Bcable%2Caps%2C144&sr=8-3&th=1) to connect the Open Ephys I/O board to the Open Ephys acquisition board.
6. Intan Technologies RHD 6 ft ultra thin SPI [cable](https://intantech.com/RHD_SPI_cables.html?tabSelect=RHDSPIcables) for ephys data.

## Full Rig

<p align="center">
<img width="300" height="500" src="../assets/mazeFrontView.png"> 
</p>




