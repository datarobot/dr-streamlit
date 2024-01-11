#
#  Copyright 2023 DataRobot, Inc. and its affiliates.
#
#  All rights reserved.
#  This is proprietary source code of DataRobot, Inc. and its affiliates.
#  Released under the terms of DataRobot Tool and Utility Agreement.
#
import pytest
import responses
from click.testing import CliRunner
from responses import matchers

from drapps.ls import ls


@responses.activate
@pytest.mark.parametrize('ids_only', (False, True))
def test_ls_apps(api_endpoint_env, api_token_env, ids_only):
    applications_list_data = {
        'count': 3,
        'data': [
            {
                'id': '65980d79eea4fd0eddd59bba',
                'name': "App 1",
                'status': 'running',
                'applicationUrl': 'http://ho.st/custom_applications/65980d79eea4fd0eddd59bba/',
                'envVersionId': '659964572522de6a026de5cf',
            },
            {
                'id': '659964182522de6a026de5cd',
                'name': "App 2",
                'status': 'running',
                'applicationUrl': 'http://ho.st/custom_applications/659964182522de6a026de5cd/',
                'envVersionId': '659964572522de6a026de5d0',
            },
            {
                'id': '659964382522de6a026de5ce',
                'name': "App 3",
                'status': 'running',
                'applicationUrl': 'http://ho.st/custom_applications/659964382522de6a026de5ce/',
                'envVersionId': '659964572522de6a026de5d1',
            },
        ],
    }
    if ids_only:
        expected_output = (
            '65980d79eea4fd0eddd59bba 659964182522de6a026de5cd 659964382522de6a026de5ce\n'
        )
    else:
        expected_output = (
            'id                        name    status    applicationUrl\n'
            '------------------------  ------  --------  ----------------------------------------------------------\n'
            '65980d79eea4fd0eddd59bba  App 1   running   http://ho.st/custom_applications/65980d79eea4fd0eddd59bba/\n'
            '659964182522de6a026de5cd  App 2   running   http://ho.st/custom_applications/659964182522de6a026de5cd/\n'
            '659964382522de6a026de5ce  App 3   running   http://ho.st/custom_applications/659964382522de6a026de5ce/\n'
        )

    app_list_url = f'{api_endpoint_env}/customApplications/'
    auth_matcher = matchers.header_matcher(
        {'Authorization': f'Bearer {api_token_env}'}
    )  # checker for API token
    responses.get(app_list_url, json=applications_list_data, match=[auth_matcher])

    runner = CliRunner()
    cli_args = ['apps']
    if ids_only:
        cli_args.append('--id-only')
    result = runner.invoke(ls, cli_args)

    assert result.exit_code == 0
    assert result.output == expected_output


@responses.activate
@pytest.mark.parametrize('ids_only', (False, True))
def test_ls_envs(api_endpoint_env, api_token_env, ids_only):
    execution_envs_list_data = {
        'count': 3,
        'data': [
            {
                'id': '659966682522de6a026de5d2',
                'name': 'Env 1',
                'description': 'First example',
                'programmingLanguage': 'python',
            },
            {
                'id': '659966682522de6a026de5d3',
                'name': 'Env 2',
                'description': 'Second example',
                'programmingLanguage': 'python',
            },
            {
                'id': '659966682522de6a026de5d4',
                'name': 'Env 3',
                'description': 'Third example',
                'programmingLanguage': 'python',
            },
        ],
    }
    if ids_only:
        expected_output = (
            '659966682522de6a026de5d2 659966682522de6a026de5d3 659966682522de6a026de5d4\n'
        )
    else:
        expected_output = (
            'id                        name    description\n'
            '------------------------  ------  --------------\n'
            '659966682522de6a026de5d2  Env 1   First example\n'
            '659966682522de6a026de5d3  Env 2   Second example\n'
            '659966682522de6a026de5d4  Env 3   Third example\n'
        )

    app_list_url = f'{api_endpoint_env}/executionEnvironments/'
    auth_matcher = matchers.header_matcher(
        {'Authorization': f'Bearer {api_token_env}'}
    )  # checker for API token
    params_matcher = matchers.query_param_matcher(
        {'useCases': 'customApplication'}
    )  # check that filter by use cases was used
    responses.get(app_list_url, json=execution_envs_list_data, match=[auth_matcher, params_matcher])

    runner = CliRunner()
    cli_args = ['envs']
    if ids_only:
        cli_args.append('--id-only')
    result = runner.invoke(ls, cli_args)

    assert result.exit_code == 0
    assert result.output == expected_output
