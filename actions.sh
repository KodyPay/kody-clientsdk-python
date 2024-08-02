#!/bin/zsh

git clone https://github.com/KodyPay/kp-protocols-clientsdk.git
cp -Rf kp-protocols-clientsdk/src/main/proto proto
rm -rf kp-protocols-clientsdk
mkdir generated
find ./proto -name "*.proto" -print0 | xargs -0 python -m grpc_tools.protoc -I./proto --python_out=./generated --grpc_python_out=./generated
rm -rf proto
find "generated/com/kodypay/grpc/" -type d -not -name '__pycache__' -exec touch {}/__init__.py \;
echo "__version__ = '0.0.1'" > generated/com/kodypay/grpc/__init__.py
mkdir kody_clientsdk_python
cp -R generated/com/kodypay/grpc/* kody_clientsdk_python
rm -rf generated
find ./kody_clientsdk_python -type f -name "*.py" -exec sed -i '' -e '/^import / s/com\.kodypay\.grpc/kody_clientsdk_python/g' -e '/^from / s/com\.kodypay\.grpc/kody_clientsdk_python/g' {} \;