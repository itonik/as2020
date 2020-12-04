# Asyncio

## Запуcк c virtual environment:

```[shell]
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
./serve.sh
```

(На Windows активация venv: venv\Scripts\deactivate.bat)

## Основы asyncio

Чтобы пользоваться asyncio достаточно понять несколько простых концептов:

1. Корутина - функция с `async` в объявлении. В отличии от обычной
фунции её необходимо запускать с помощью await либо create_task

```[python3]
async def coroutine(arg):
    print(f'Hello {arg}. Starting...')
    asyncio.sleep(2)
    print('done')
```

2. `await` - дождаться выполнения корутины

```[python3]
await coroutine('programmer')
print('Awaited')

# > Hello programmer. Starting...
# (2sec pause)
# > done
# > Awaited
```

3. `asyncio.create_task()`: не ждать выполнения корутины, запустить корутину "в фоне"

```[python3]
asyncio.create_task(coroutine('hacker'))
print('Not waiting')

# > Hello hacker. Starting...
# > Not waiting
# (2sec pause)
# > done
```

4. `Queue` - очередь, новые элементы в которой можно ожидать (await)

```[python3]
new_element = await queue.get()

# Put в очереди тоже необходимо ждать (если очередь переполнена)
await queue.put(new_element)
```

5. `asyncio.run()`: как await только в не асинхроном контексте. В server.py не нужна так как сам асинхронный контекст создаётся ASGI сервером (uvicorn)
