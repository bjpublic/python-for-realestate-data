
aws ecr get-login-password --region ap-northeast-2 | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.ap-northeast-2.amazonaws.com


docker build -t test_image:tag1 .

docker tag test_image:tag1 $ACCOUNT_ID.dkr.ecr.ap-northeast-2.amazonaws.com/python-apart:tag1

docker push $ACCOUNT_ID.dkr.ecr.ap-northeast-2.amazonaws.com/python-apart:tag1

