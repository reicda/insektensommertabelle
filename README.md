[![Gitpod Ready-to-Code](https://img.shields.io/badge/Gitpod-Ready--to--Code-blue?logo=gitpod)](https://gitpod.io/#https://github.com/BjoernSchilberg/insektensommertabelle)


# Insektensommer Tabelle

- [Insektensommer Tabelle](#insektensommer-tabelle)
  - [Project setup](#project-setup)
    - [Compiles and hot-reloads for development](#compiles-and-hot-reloads-for-development)
    - [Compiles and minifies for production](#compiles-and-minifies-for-production)
    - [Run your tests](#run-your-tests)
    - [Lints and fixes files](#lints-and-fixes-files)
    - [Customize configuration](#customize-configuration)
  - [Publish on github pages](#publish-on-github-pages)
  - [FTP connection](#ftp-connection)

## Project setup

```shell
yarn install
```

### Compiles and hot-reloads for development

```shell
yarn run serve
```

### Compiles and minifies for production

```shell
yarn run build
```

### Run your tests

```shell
yarn run test
```

### Lints and fixes files

```shell
yarn run lint
```

### Customize configuration

See [Configuration Reference](https://cli.vuejs.org/config/).

## Publish on github pages

Publish on github pages is handling via github actions by pushing tags
following [SemVer vX.Y.Z](https://semver.org/).

```shell
git tag vX.Y.Z
git push origin --tags
```

## FTP connection

```shell
ncftp -u $FTP_USER -p $FTP_PASSWORD $FTP_SERVER
```

```shell
ncftp -u $FTP_USER -p $FTP_PASSWORD ftp://$FTP_SERVER/insektensommertabelle
```