# Description

### 数据库 

#### 表 'vehicle_records'

| 键名                   	| 类型         	| 说明                                                                                                    	|
|------------------------	|--------------	|---------------------------------------------------------------------------------------------------------	|
| id                     	| int          	| 主键表ID                                                                                                	|
| uniqueID               	| varchar(128) 	| 记录唯一ID                                                                                              	|
| cameraUID              	| varchar(128) 	| 相机唯一ID                                                                                              	|
| laneNumber             	| int          	| 车道号 [1, 2, 3, 4....]                                                                                 	|
| direction              	| int          	| 行驶方向 [0: 未知, 1: 向上, 2: 向下, 3: 向左, 4: 向右]                                                  	|
| checkPointTime         	| int          	| 这辆过相机时间, 用unix时间戳表示, 精确到秒                                                  	|
| vehicleClassConfidence 	| int          	| 车辆类型识别可信度 [0~100] 0为完全不可信 100为完全可信                                                  	|
| vehicleClassId         	| int          	| 车辆类型 [0~9] 0:轿车 1:大客车 2:小客车 3:面包车 4:小型货车 5:中型货车 6:大型货车 7:危化品车 8:其他车辆 	|
| speedKmh               	| double       	| 车速 单位: 公里/小时                                                                                    	|
| plateConfidence        	| int          	| 车牌识别可信度 [0~100] 0为完全不可信 100为完全可信                                                      	|
| plateType              	| varchar(128) 	| 车牌类型                                                                                                	|
| plateColor             	| varchar(128) 	| 车牌颜色                                                                                                	|
| license                	| varchar(128) 	| 车牌号                                                                                                  	|

#### 表 'photo'

| 键名        	| 类型         	| 说明                        	|
|-------------	|--------------	|-----------------------------	|
| id          	| int          	| 主键表ID                    	|
| name        	| varchar(128) 	| 图片文件名                  	|
| thumbnail   	| varchar(128) 	| 缩略图文件名                	|
| record_id   	| int          	| 外键指向vehicle_records表id 	|
| upload_time 	| datetime     	| 上传时间                    	|

