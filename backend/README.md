## Setting up
### Make sure python 3.8 is installed

### Create .env file in `backend` directory (see `env.example`)

```shell
cd backend
pip install poetry==1.1.11
poetry install
```

# Download [model](https://downloader.disk.yandex.ru/disk/5e3bc01bb3d2a4e494efdd7c04068992678782972d7a8702c261b1abb9994570/61a0acfa/cLkIShqMBVOfwdgjZNfWTasgaDK39AS7Rlg5i6deYEa5McyVOdD1uoNebHzEltay-INl8dio2n2MpNFyEctQrA%3D%3D?uid=0&filename=vox-cpk.pth.tar&disposition=attachment&hash=p%2Bs5J2CIkLAe/aDBvvSnnPvWfl49eJ/Eu%2BGelUjS937Fz5Ko4KEmpsZE%2BRQ7wgUbq/J6bpmRyOJonT3VoXnDag%3D%3D%3A/vox-cpk.pth.tar&limit=0&content_type=application%2Foctet-stream&owner_uid=225219335&fsize=728766691&hid=558af945c202c1c577538def4acf9fcc&media_type=compressed&tknv=v2) and put it in `models` dir

#if this link does not work, manualy download vox-cpk.pth.tar from [here] (https://drive.google.com/drive/folders/1PyQJmkdCsAkOYwUyaj_l-l0as-iLDgeH) or [here] (https://yadi.sk/d/lEw8uRm140L_eQ) then scp to server and put in `models` dir


# Running project locally
```shell
cd backend
poetry run python main.py
```

# Documentation 

http://localhost:8001/docs

## docker 

docker build --rm -t donft-backend:latest .

docker run --env-file .env --rm  -p 2800:2800 --name donft-backend donft-backend:latest 
