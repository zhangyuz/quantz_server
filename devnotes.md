## RESTFul API 设计

https://api.xxx.com/v1/endpoints?page=1&perpage=20
1. 必须使用HTTPS
2. api 要使用独立的域名
3. 建议在地址中增加 API 的版本
4. endpoints 表示API的具体地址，表示一种资源（因此不能包含动词），只能使用名词，通常与数据库表格名称对应。使用复数单次，表示数据集合。
5. ?page=1&perpage=20 用来过滤信息。
6. HTTP 动词
    - GET（SELECT）：从服务器取出资源（一项或多项）。
    - POST（CREATE）：在服务器新建一个资源。
    - PUT（UPDATE）：在服务器更新资源（客户端提供改变后的完整资源）。
    - PATCH（UPDATE）：在服务器更新资源（客户端提供改变的属性）。
    - DELETE（DELETE）：从服务器删除资源。
7. 正常返回状态码：
    - 200 OK - [GET]：服务器成功返回用户请求的数据，该操作是幂等的（Idempotent）。
    - 201 CREATED - [POST/PUT/PATCH]：用户新建或修改数据成功。
    - 202 Accepted - [*]：表示一个请求已经进入后台排队（异步任务）
    - 204 NO CONTENT - [DELETE]：用户删除数据成功。
    - 400 INVALID REQUEST - [POST/PUT/PATCH]：用户发出的请求有错误，服务器没有进行新建或修改数据的操作，该操作是幂等的。
    - 401 Unauthorized - [*]：表示用户没有权限（令牌、用户名、密码错误）。
    - 403 Forbidden - [*] 表示用户得到授权（与401错误相对），但是访问是被禁止的。
    - 404 NOT FOUND - [*]：用户发出的请求针对的是不存在的记录，服务器没有进行操作，该操作是幂等的。
    - 406 Not Acceptable - [GET]：用户请求的格式不可得（比如用户请求JSON格式，但是只有XML格式）。
    - 410 Gone -[GET]：用户请求的资源被永久删除，且不会再得到的。
    - 422 Unprocesable entity - [POST/PUT/PATCH] 当创建一个对象时，发生一个验证错误。
    - 500 INTERNAL SERVER ERROR - [*]：服务器发生错误，用户将无法判断发出的请求是否成功。
8. 如果返回状态码4XX，应该同时返回错误信息
   `{error:"invalid api key"}`
9. 返回的数据结果应该符合以下规范
   - GET /collection：返回资源对象的列表（数组）
   - GET /collection/resource：返回单个资源对象
   - POST /collection：返回新生成的资源对象
   - PUT /collection/resource：返回完整的资源对象
   - PATCH /collection/resource：返回完整的资源对象
   - DELETE /collection/resource：返回一个空文档
11. Hypermedia API,文档中有一个link属性，用户读取这个属性就知道下一步该调用什么API了。rel表示这个API与当前网址的关系（collection关系，并给出该collection的网址），href表示API的路径，title表示API的标题，type表示返回类型
```JSON
{"link": {
  "rel":   "collection https://www.example.com/zoos",
  "href":  "https://api.example.com/zoos",
  "title": "List of zoos",
  "type":  "application/vnd.yourformat+json"
}}
```
11. 认证使用OAuth2.0 。