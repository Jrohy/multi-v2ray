@echo off
echo 更新依赖中...
pip install -U setuptools wheel twine
echo 打包中...
python setup.py sdist bdist_wheel
echo 上传包...
twine upload dist/*
echo 清理打包环境..
if exist dist (
	rd /s /Q build
    rd /s /Q dist
    rd /s /Q v2ray_util.egg-info
    rd /s /Q v2ray_util\__pycache__
)
echo 打包完成!
pause