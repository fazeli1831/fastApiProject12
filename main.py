from fastapi import FastAPI, HTTPException
import multiprocessing
import time

app = FastAPI()

def foo():
    print('Starting function')
    for i in range(0, 10):
        print('-->%d\n' % i)
        time.sleep(1)
    print('Finished function')

@app.get("/run-process")
async def run_process():
    p = multiprocessing.Process(target=foo)
    print('Process before execution:', p, p.is_alive())
    p.start()
    print('Process running:', p, p.is_alive())
    time.sleep(2)  # Allow the process to run for 2 seconds
    print('Process terminated:', p, p.is_alive())
    p.terminate()
    p.join()
    print('Process joined:', p, p.is_alive())
    return {
        "process_id": p.pid,
        "is_alive": p.is_alive(),
        "exit_code": p.exitcode
    }

@app.get("/run-process/{seconds}")
async def run_process_with_seconds(seconds: int):
    p = multiprocessing.Process(target=foo)
    p.start()
    time.sleep(seconds)  # Allow the process to run for 'seconds' before terminating
    p.terminate()
    p.join()
    return {
        "process_id": p.pid,
        "is_alive": p.is_alive(),
        "exit_code": p.exitcode
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
