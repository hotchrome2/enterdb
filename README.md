# enterdb

## 既存のテーブル紐づけ問題

https://stackoverflow.com/questions/39955521/sqlalchemy-existing-database-query
https://qiita.com/takada-at/items/9f008e8f394235b72c6e

https://docs.sqlalchemy.org/en/14/core/reflection.html#overriding-reflected-columns
変更しないカラムは書かなくてよい。これは良い。

## Upload

https://qiita.com/XPT60/items/1ae2bb99e81bd8c8bc98 一時ファイル保存

### content_type

https://fastapi.tiangolo.com/tutorial/request-files/#uploadfile


### 422 Unprocessable Entity

INFO:     127.0.0.1:52103 - "POST /upload/?user_id=2 HTTP/1.1" 422 Unprocessable Entity
が出てこまる

https://blog.stu345.com/fastapi-post-file_and_model/ FastAPIで画像とモデルを同時にpostする
https://stackoverflow.com/questions/65504438/how-to-add-both-file-and-json-body-in-a-fastapi-post-request/67106597#67106597
↑結局これが直接役立った。

https://stackoverflow.com/questions/60127234/how-to-use-a-pydantic-model-with-form-data-in-fastapi
Swaggerでもちゃんとしたいとき？




## Blog Upload
https://docs.microsoft.com/ja-jp/azure/storage/blobs/storage-quickstart-blobs-python?tabs=environment-variable-windows
https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/storage/azure-storage-blob/samples



end