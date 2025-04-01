# Automated Maze (under development)

This tutorial describes how we built our autoamted maze in the Niell Lab.

***Important: this tutorial is currently under development***

<p align="center">
<img width="500" height="300" src="../assets/mazeTopView.png">
<img width="500" height="300" src="../assets/mazeComponents.png">
</p>

# Components

## Maze

1. 1" T-slotted [squared](https://www.mcmaster.com/47065T101/) and [rounded](https://www.mcmaster.com/3136N27/) framing rails, cut to a custom size with 1/4"-20 threads on both ends.
2. Sign white 9 % light transmission [acrylic](https://www.tapplastics.com/product/plastics/cut_to_size_plastic/acrylic_sheets_color/341) for the floor and walls of the maze.
3. 1" [brakets](https://www.mcmaster.com/47065T236/) and [cubes](https://www.mcmaster.com/47065T244/) to assemble the structural frame of the maze.
4. A white melamine [wood shelf](https://www.homedepot.com/p/White-Melamine-Wood-Shelf-23-75-in-D-x-48-in-L-252297/202089063) with 2" [caster wheels](https://www.amazon.com/Casters-Locking-Castors-Furniture-Kitchen/dp/B09QZMTSCQ/ref=pd_bxgy_img_d_sccl_2/142-9516444-0421340?pd_rd_w=h5m3x&content-id=amzn1.sym.839d7715-b862-4989-8f65-c6f9502d15f9&pf_rd_p=839d7715-b862-4989-8f65-c6f9502d15f9&pf_rd_r=FRMHFY3ZBWA5QW7X6ASM&pd_rd_wg=8v5Oh&pd_rd_r=5618abc9-7d00-4d7a-a696-668fa49b88b9&pd_rd_i=B0BFXLTQNH&th=1) for the base of the maze.
5. A 10" [screen](https://www.amazon.com/dp/B0987468N2/ref=sspa_dk_detail_4?pd_rd_i=B0987468N2&pd_rd_w=QqC5K&content-id=amzn1.sym.386c274b-4bfe-4421-9052-a1a56db557ab&pf_rd_p=386c274b-4bfe-4421-9052-a1a56db557ab&pf_rd_r=1QH3Q0EH5X5P3PGTJ3EK&pd_rd_wg=wrki0&pd_rd_r=280cd8b9-b4b4-4a81-84ca-9a71bb273634&s=pc&sp_csd=d2lkZ2V0TmFtZT1zcF9kZXRhaWxfdGhlbWF0aWM&th=1) for displaying visual stimuli.
6. Mini USB [speaker](https://www.adafruit.com/product/3369?gclid=Cj0KCQjw9fqnBhDSARIsAHlcQYQN7-PUcKRt7g5K4LZLOxeUrOmGBO-mkdPEippvQnJ8RdAV6c8ZS8oaAvPWEALw_wcB) for signaling correct and incorrect trials.
7. Diffused 5 mm [LEDs](https://www.adafruit.com/product/4203?gclid=Cj0KCQjw9fqnBhDSARIsAHlcQYQOVymyhPb8JML-s9yA5havhJG0yBzvc3udh55acPwMJ-_8xEU4wKcaAnpeEALw_wcB) for signaling correct trials.
8. [Solenoid valves](https://www.theleeco.com/industries/scientific-instruments/products/solenoid-valves/browse/?filters[subtype][]=Control+Solenoid+Valves) for control of water delivery.
9. 1/16" ID x 1/8" OD Tygon [tubing](https://www.usplastic.com/catalog/item.aspx?itemid=91104&catid=864) for the water delivery system.
10. 14 gauge luer-lock blunt tip [needles](https://www.amazon.com/Syringe-Dispensing-Needles-Length-Interface/dp/B07DZC225B/ref=pd_ci_mcx_di_int_sccai_cn_d_sccl_2_1/133-0408013-9182656?pd_rd_w=JuARf&content-id=amzn1.sym.751acc83-5c05-42d0-a15e-303622651e1e&pf_rd_p=751acc83-5c05-42d0-a15e-303622651e1e&pf_rd_r=SDJGVFYGQZ0KS2EZG109&pd_rd_wg=XP1nb&pd_rd_r=9ea53b80-e963-4a30-bfc5-857ae6b058f9&pd_rd_i=B07DZC225B&psc=1) as spouts for water delivery.

## Automated Doors

1. [Pneumatic actuators](https://www.amazon.com/Baomain-Pneumatic-Cylinder-SC-Screwed/dp/B01F9XZQ1K/ref=pd_ci_mcx_di_int_sccai_cn_d_sccl_2_2/136-8001444-7379768?pd_rd_w=CoJWI&content-id=amzn1.sym.751acc83-5c05-42d0-a15e-303622651e1e&pf_rd_p=751acc83-5c05-42d0-a15e-303622651e1e&pf_rd_r=AXNT0SNVR13YJT89ZTJJ&pd_rd_wg=F8NEU&pd_rd_r=9dcf470c-de43-4689-a980-ca5e8e994869&pd_rd_i=B01F9XZQ1K&th=1) for movement of the automated doors.
2. A [solenoid manifold](https://www.amazon.com/Baomain-4V210-08-Position-Pneumatic-Solenoid/dp/B01D9IGCTC/ref=sims_dp_d_dex_ai_speed_loc_mtl_v4_d_sccl_4_1/136-8001444-7379768?pd_rd_w=QAJm3&content-id=amzn1.sym.af515e1d-64ab-47a5-8a2e-6be4d0f4cdc5&pf_rd_p=af515e1d-64ab-47a5-8a2e-6be4d0f4cdc5&pf_rd_r=QQ6ZJF00XSNFZP6H8B3Z&pd_rd_wg=ip6Yj&pd_rd_r=6282a60c-3df6-4d58-8258-af29a286d7ae&pd_rd_i=B01D9IGCTC&psc=1) for controlling the automated doors.
3. [6 mm](https://www.amazon.com/Tailonz-Pneumatic-Black-Polyurethane-32-8ft/dp/B08GC6TR2S/ref=sr_1_6?crid=B4SJCL6S8C9C&dib=eyJ2IjoiMSJ9.DejGkL7N9ogqAzdCGOySW8Ul4oFXYI6uTvpMsLFLQavsPcgyc9dCZSS0RZEDuOVTGBNc74dp5AgyndprPP87Hf5uJyTtiH9rcP7fQU8OTkzCA8K8Lv6_3velU18rnE5GaAfLZ6q1gyariRIkULl7URyfKc2KDw0pVo_LMPqGbvt8MmwsfXPHnCfzkYaMb4eLXCrkmvK0VoPedBBdU368PWvUj1i6hELtX5D_il5MeDzO23k3WryqV_aB2wbEvVOaP6Nks4V_xsxegeLF3uYnt_uTJ9Vwoqsxe3ukTBuhLVI.ajZ5AaE_mu1l8TI9caTWLeYIIOOZVvQAvAvGWvogzXg&dib_tag=se&keywords=Air%2BLine%2BTubing%2BKit%2B6mm%2Bblack&qid=1714772204&s=industrial&sprefix=air%2Bline%2Btubing%2Bkit%2B6mm%2Bblac%2Cindustrial%2C121&sr=1-6&th=1) and [8 mm](https://www.amazon.com/CGELE-Pneumatic-Transfer-OD-39-4Ft-12Meter/dp/B09LS1S7MK/ref=sr_1_3?crid=1UCLWG8RC00F5&dib=eyJ2IjoiMSJ9.9IT0mdNrbcPPwFnwS3lttd1-X4Lt2TRh2Ekuy9jjREetTrO9R6abyOPbWKJOIBw0.COukHekBEaDTeMd4yj45MHDLXDYYBJPRxJqthZbJgoc&dib_tag=se&keywords=TAILONZ%2BPNEUMATIC%2BBlack%2B5%2F16&qid=1724450805&s=hi&sprefix=tailonz%2Bpneumatic%2Bblack%2B5%2F1%2Ctools%2C144&sr=1-3&th=1) tubing for air connections, as well as [adapters](https://www.amazon.com/Metalwork-Straight-Reducing-Pneumatic-Connector/dp/B07C7BGQ9S/ref=sr_1_5?crid=2EOM3OXEO5504&dib=eyJ2IjoiMSJ9.sZVireplGplt2H6sWKEogbyxddOqDaPAou-Hecj9GtV1WioAia-WJQIGtxOWdVFVTQup_Kqhm3tuUmI4i797ggSqxKtK6BQcITqGEm_J8Jd80-lc9OO1TKfBGQq-wL9LLAby1xOZYYVYpjkhlgDVuNfve2of7sbq0TFmEraXme2kNnz8YlwITV7zWLn_CfpviRaNwQc0ZqtmgVXMZVcHYADlHSF5U06SYpBPrxmvLaM.iJ10JiNAwGi4COcf2CwCBSLYdg1aO_1qU6pIi8fo8Nk&dib_tag=se&keywords=10%2Bmm%2Bto%2B6%2Bmm%2Bair%2Btubing%2Badapter&qid=1724450958&sprefix=10%2Bmm%2Bto%2B6%2Bmm%2Bair%2Btubing%2Badapter%2Caps%2C214&sr=8-5&th=1).
4. A [regulator](https://www.amazon.com/dp/B09MLMFF2K/ref=sspa_dk_detail_4?pd_rd_i=B09MLMFF2K&pd_rd_w=U3UuV&content-id=amzn1.sym.8c2f9165-8e93-42a1-8313-73d3809141a2&pf_rd_p=8c2f9165-8e93-42a1-8313-73d3809141a2&pf_rd_r=DGYB1C9ZMZ9F3ED5QBE2&pd_rd_wg=BIhvv&pd_rd_r=dd296391-c469-481f-a3ac-71e60c75697b&s=industrial&sp_csd=d2lkZ2V0TmFtZT1zcF9kZXRhaWw&th=1) for setting the input air pressure to the solenoid manifold.
5. IR [beam breaks](https://www.adafruit.com/product/2167) for detecting the mouse traverse through the maze.
6. 100 cm M/M [wires](https://www.amazon.com/EDGELEC-Breadboard-Optional-Assorted-Multicolored/dp/B07GD1W7XV/ref=sr_1_1_sspa?crid=1D6I1EZM32X2T&dib=eyJ2IjoiMSJ9.tjHxIQLJsk16_0YVtUGN6YeXdt0VqIwh7Zmfzd7nvfTaoSMecktPIPsgfi6eLwfPrpE-Z7TFF3Gb6OmAsEyH4OuRfeKQ2U6yeUaDnbuFGswrOXPukg3xDJGZqP0xiogOAQo_2PqBlSW5yXpFgDqxkBzMUHsNNzfc4F-zrGIxkpvzX6CnOzBpjidBHCxZRSphsHbICibgDRfXkQytRIVXbw9Gbyz2Bt6wmlDkohLT7gUYbs8jQcpc5IITMBIXfrioVjBJ50nB4BJkOvXv_kzaIx5H3ulgZPomOofbuDLn7Cw.BAJcuUxcOIL5un-H80QwuIrBCIlUhJ-gg4DElPhICeA&dib_tag=se&keywords=jumper%2Bwires&qid=1718926518&s=industrial&sprefix=jumper%2Bwire%2Cindustrial%2C148&sr=1-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1) and 1" F/F [wires](https://www.digikey.com/en/products/detail/pololu-corporation/3860/10451018) for connections between IR sensors, water valves and LEDs to the Teensy circuit.
7. 12" M/M [wires](https://www.digikey.com/en/products/detail/pololu-corporation/1765/10450795) and 2" M/F [wires](https://www.digikey.com/en/products/detail/pololu-corporation/3845/10451009) for connections between the solenoid manifold and the Teensy circuit.

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

## Mouse Cameras and Inertial Measurement Unit (IMU)

1. [Video capture devices](https://www.amazon.com/StarTech-com-USB3HDCAP-Video-Capture-Device/dp/B00PC5HUA6/ref=sr_1_3?crid=1AFS4ZNT5DLU3&dib=eyJ2IjoiMSJ9.2LWQRFf16ZPMxyykpqUm1QtyUSt6AnmngN9oj-gAVxMcaWOHj-sg9mHyR_VOyZlGUHDAgP-RiLVpqHIJ-4CsqHQrcvttvKUw0d4jl_iBUglC5TElRCm2L9J60tKoq5Ut_k4KGTKNtWHq8QpZT8mpwddy7JufOzukyDw1aMnpO24DBLibw6otOFhMhWo_Zq9ubgKt0tLhXP5yMT88ZsZAhWJNJHszQvsijkaGipRK1V4.3MNmDwkGFHCEMfpO7wPUEYZ5Zc35iEvtZ5vzg5dQjI0&dib_tag=se&keywords=startech+usb+3.0+hd+video+capture+device+1080p&qid=1743533019&sprefix=startech+usb+3.0+hd+video+capture+device+1080p%2Caps%2C130&sr=8-3) for converting analog video from both the eye and the world cameras into digital video.
2. An analog 5 mm x 5 mm [camera](https://www.aliexpress.us/item/3256803738909660.html?spm=a2g0o.detail.pcDetailTopMoreOtherSeller.10.47a4Gmv2Gmv2Vk&gps-id=pcDetailTopMoreOtherSeller&scm=1007.40196.422467.0&scm_id=1007.40196.422467.0&scm-url=1007.40196.422467.0&pvid=40156854-8944-49dc-8f22-28e36af707d0&_t=gps-id:pcDetailTopMoreOtherSeller,scm-url:1007.40196.422467.0,pvid:40156854-8944-49dc-8f22-28e36af707d0,tpp_buckets:668%232846%238108%231977&pdp_ext_f=%7B%22order%22%3A%2273%22%2C%22eval%22%3A%221%22%2C%22sceneId%22%3A%2230050%22%7D&pdp_npi=4%40dis%21USD%2117.62%2110.12%21%21%2117.62%2110.12%21%402101c5b217435439061578444e0ef5%2112000027485322782%21rec%21US%21%21ABXZ&utparam-url=scene%3ApcDetailTopMoreOtherSeller%7Cquery_from%3A) for recoridng the eye of the mouse.
3. TDK InvenSense [inertial measurement unit](https://invensense.tdk.com/products/motion-tracking/9-axis/icm-20948/) for measuring the position of the head of the mouse.
4. Intan Technologies RHD 6 ft ultra thin SPI [cable](https://intantech.com/RHD_SPI_cables.html?tabSelect=RHDSPIcables) for video and IMU data.

## Electrophysiology

1. Open Ephys [acquisition board](https://open-ephys.org/acquisition-system/oeps-9029).
2. Open Ephys [I/O Board](https://open-ephys.org/acquisition-system/io-board-pcb), with through-hole vertical female [BNC connectors](https://www.peconnectors.com/coaxial-rf-connectors-bnc-f-rca/hws3912/?srsltid=AfmBOoo6W5EEuw7a9Wj3TCphOwvCRphM8mKeDhZolUMiHQv2XTFZ-yY3QIs&gQT=1) and a surface-mount [HDMI connector](https://www.digikey.com/en/products/detail/amphenol-cs-fci/10029449-111RLF/2785386?s=N4IgTCBcDaIGwAYCcBaALHAjGlmUDkAREAXQF8g) for connection between the RoSco head motion tracking device and the Open Ephys acquisition board.
3. A male DB15 to terminal breakout board [connector](https://www.amazon.com/DB15-Breakout-Connector-Pin-Male/dp/B073RGHNVD) for connections between single pins to the Open Ephys I/O board.
4. A male to female DB15 [cable](https://www.amazon.com/Female-Extension-tinned-Shielded-soliConnector/dp/B093P4W22V/ref=sr_1_5?crid=130GIODUV9ZMD&dib=eyJ2IjoiMSJ9.8Dfuw8gbwaj0Ltt9hNVz6aKSq_yqtXQj2jlV4QmFc4y4sT0Htf3cpZzMWrKl_7DuRt3OoqQtyYHA00QE4swo7XOP6aDjIESvzWZJz_AbNq9HKS9-otb72Ef0sy9F2O8FNDBNScFXaFDjZ9bGLp1yK329s55HWbS-tm0ppJejqisqmffPmw2CRpsBq8liHvQWkC3pBj9iQ86vSZMEVUKZuIpHASC8Zus6WETTaYYXqhI.G9BbIbfxLHvFTva8zR1PQ_lCHkEM7KjyQC1bDxgmQvE&dib_tag=se&keywords=db15%2Bcable%2Bmale%2Bto%2Bfemale%2B3%2Bft&qid=1742251738&sprefix=db15%2Bcable%2Bmale%2Bto%2Bfemale%2B3%2Bft%2Caps%2C152&sr=8-5&th=1) to connect the RoSco head motion tracking device to the Open Ephys I/O board.
5. Intan Technologies RHD 6 ft ultra thin SPI [cable](https://intantech.com/RHD_SPI_cables.html?tabSelect=RHDSPIcables) for ephys data.

## Rig

<p align="center">
<img width="300" height="500" src="../assets/mazeFrontView.png"> 
</p>




