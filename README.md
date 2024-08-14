# Fórmula 1

## Iniciar Projeto

Rodar o seguinte comando:

```shell
docker-compose build
```

Iniciar o Banco de Dados postgres:

```shell
docker-compose exec web bash
```

E rodar o seguinte comando:

```shell
alembic upgrade head
```
