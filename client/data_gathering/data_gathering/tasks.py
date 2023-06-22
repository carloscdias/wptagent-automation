from urllib.parse import urlparse
from scipy.stats import expon
from data_gathering.celery import app, logger, QUEUE
from .utils import *

EXPONENTIAL_MEAN_EXPERIMENTO_1_INTERVAL = 30

@app.task(name='data_gathering.traceroute')
@app.task(name=f'{QUEUE}.data_gathering.traceroute')
def traceroute(domain):
    output = call_traceroute(domain)
    logger.info(output)

@app.task(name='data_gathering.ndt7')
@app.task(name=f'{QUEUE}.data_gathering.ndt7')
def ndt7():
    output = call_ndt7()
    logger.info(output)


@app.task(name=f'{QUEUE}.data_gathering.get_version')
def get_version():
    return get_runtime_version()

@app.task(name='data_gathering.get_queue')
def get_queue():
    return QUEUE

@app.task(name='data_gathering.experimento_1')
@app.task(name=f'{QUEUE}.data_gathering.experimento_1')
def experimento_1():
    """
    Ordem de execução:
        - agenda a próxima execução do experimento de acordo com ~exp(30)
        - tira na moeda entre setupNavigationFilePath e setupReproductionFilePath -> X
        - realiza o setup do teste X (obtém url)
        - traceroute
        - realiza o teste X no selenium
        - realiza o teste X no puppeteer
        - realiza o teste ndt
    """
    result = {
        'started': None,
        'mac': QUEUE[4:],
    }
    # agenda APS
    time_in_minutes = expon.rvs(scale=int(EXPONENTIAL_MEAN_EXPERIMENTO_1_INTERVAL), size=1)[0]
    logger.info(f'Next execution: {time_in_minutes}')
    # navigation or reproduction?
    experiment = get_experiment_type_at_random()
    result['experiment'] = experiment
    # setup
    url = get_url_for_experiment_type(experiment)
    use_adblock = random.random() < 0.5
    resolution_type = '1' if random.random() < 0.5 else '2'
    result['url'] = url
    result['use_adblock'] = use_adblock
    result['resolution_type'] = resolution_type
    # traceroute
    domain = urlparse(url).netloc
    traceroute_result = call_traceroute(domain)
    result['traceroute'] = traceroute_result
    # browser experiments
    result['browser'] = {}
    browser_experiments = get_browser_experiment_func(experiment)
    for method, run_func in zip(['selenium', 'puppeteer'], browser_experiments):
        result['browser'][method] = run_func(url, use_adblock, resolution_type)
    # ndt
    ndt_result = call_ndt7()
    result['ndt_result'] = ndt_result
    return result
