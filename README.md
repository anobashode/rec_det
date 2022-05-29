# rec_det
run App.py in anaconda -> up backend
then in my app terminal -> npm install -> npm start
**CHANGE STR_PATH TO IMAGE PATH TO IDENTIFY PERSON, THE CODE WORKS PERFECTLY INDEPENDENTLY**
1. manually change haar cascade classifier path in fc_det for face detection to work
2. in delivery page if already delivered orderID path added -> shows order already delivered
3. in delivery page if orderID doesnt exist, it shows
4. face recognition works independently
5. i have hardcoded only hiya.jpeg for face recognition.

......
[sql table for refer.docx](https://github.com/anobashode/rec_det/files/8794179/sql.table.for.refer.docx)
........
2/3-> sql queries
INSERT INTO PRJ_01_IIT.CONSIGNMENT_DETAIL (V_PACKAGE_ID, V_DEL_TO_NAME, V_DEL_TO_FACE) values( '58', 'yu', 'C:\Users\hiyak\Desktop\ject\my-app\validate\57yyu.jpg') ON DUPLICATE KEY UPDATE V_DEL_TO_FACE = 'C:\Users\hiyak\Desktop\ject\my-app\validate\57yu.jpg';

SELECT CASE WHEN DT.V_PACKAGE_ID IS NULL AND CD.V_PACKAGE_ID IS NOT NULL THEN 1 WHEN CD.V_PACKAGE_ID IS NULL THEN -1 ELSE 0 END AS FLAG, CASE WHEN CD.V_PACKAGE_ID IS NULL THEN 'Order ID doesn''t Exists' WHEN DT.V_PACKAGE_ID IS NULL AND CD.V_PACKAGE_ID IS NOT NULL THEN 'Order ID Exists and is not yet delivered' WHEN DT.V_PACKAGE_ID IS NOT NULL THEN 'Order ID Exists and is already delivered' END AS RESPONSE_STRING, GROUP_CONCAT(CD.V_DEL_TO_NAME) AS DELIVERY_TO_NAME_LIST FROM (SELECT SYSDATE() ) DL LEFT OUTER JOIN PRJ_01_IIT.CONSIGNMENT_DETAIL CD ON CD.V_PACKAGE_ID = '100' LEFT OUTER JOIN (SELECT DISTINCT V_PACKAGE_ID FROM PRJ_01_IIT.DELIVERED_TRANSACTIONS) DT ON CD.V_PACKAGE_ID = DT.V_PACKAGE_ID ORDER BY CD.V_DEL_TO_NAME;

select * from PRJ_01_IIT.CONSIGNMENT_DETAIL;

SELECT CASE WHEN DT.V_PACKAGE_ID IS NULL AND CD.V_PACKAGE_ID IS NOT NULL THEN 1 WHEN CD.V_PACKAGE_ID IS NULL THEN -1 ELSE 0 END AS FLAG, CASE WHEN CD.V_PACKAGE_ID IS NULL THEN 'Order ID doesn''t Exists' WHEN DT.V_PACKAGE_ID IS NULL AND CD.V_PACKAGE_ID IS NOT NULL THEN 'Order ID Exists and is not yet delivered' WHEN DT.V_PACKAGE_ID IS NOT NULL THEN 'Order ID Exists and is already delivered' END AS RESPONSE_STRING, GROUP_CONCAT(CD.V_DEL_TO_NAME) AS DELIVERY_TO_NAME_LIST FROM (SELECT SYSDATE() ) DL LEFT OUTER JOIN PRJ_01_IIT.CONSIGNMENT_DETAIL CD ON CD.V_PACKAGE_ID = '100' LEFT OUTER JOIN (SELECT DISTINCT V_PACKAGE_ID FROM PRJ_01_IIT.DELIVERED_TRANSACTIONS) DT ON CD.V_PACKAGE_ID = DT.V_PACKAGE_ID ORDER BY CD.V_DEL_TO_NAME
;

SELECT * FROM PRJ_01_IIT.CONSIGNMENT_DETAIL ;
SELECT * FROM PRJ_01_IIT.DELIVERED_TRANSACTIONS;
