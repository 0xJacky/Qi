echo "generating requirement.txt"
cd qi-server || exit
pipreqs ./ --force

cd ..
echo "building frontend"
cd qi-frontend || exit
yarn build

echo "building docker image"
cd .. || exit
docker buildx build --platform linux/arm64,linux/amd64 -t uozi/qi . --push
docker buildx build --platform linux/arm64,linux/amd64 -t registry.cn-shenzhen.aliyuncs.com/uozi/qi . --push
