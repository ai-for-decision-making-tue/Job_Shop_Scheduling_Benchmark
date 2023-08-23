import argparse
import time
import logging

from solutions.helper_functions import *
from plotting.drawer import draw_gantt_chart, draw_precedence_relations
from solutions.heuristics_scheduler.heuristics import *

logging.basicConfig(level=logging.INFO)
PARAM_FILE = "configs/basic_heuristics.toml"


def main(param_file: str = PARAM_FILE) -> None:
    """Main function to run the heuristic scheduler.

    Args:
        param_file: The parameter file to load parameters from.
    """
    start_time = time.time()
    params = load_parameters(param_file)
    env = load_job_shop_env(params['instance']['problem_instance'])

    if params['output']['plotting']:
        draw_precedence_relations(env)

    try:
        scheduler_name = params['algorithm']['scheduler_name']
        scheduler = globals()[scheduler_name]
        scheduler(env)
    except KeyError:
        logging.error(f"No scheduler found with the name {scheduler_name}")

    elapsed_time = time.time() - start_time
    logging.info("--- %s seconds ---" % elapsed_time)

    logging.info('make_span: %s', env.makespan)
    if params['output']['plotting']:
        draw_gantt_chart(env)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run heuristic scheduler")
    parser.add_argument("config_file",
                        metavar='-f',
                        type=str,
                        nargs="?",
                        default=PARAM_FILE,
                        help="path to config JSON",
                        )
    args = parser.parse_args()
    main(param_file=args.config_file)
