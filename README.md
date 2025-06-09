<div style="display: flex; align-items: center; justify-content: center; gap: 1rem;">
  <img src="./assets/hmcts-logo.png" alt="HM Courts & Tribunals Service logo" width="120" />
  <h1 style="margin: 0;">Trigger ADO Pipeline GitHub Action</h1>
</div>

Custom GitHub Action to trigger an Azure DevOps pipeline.

Ideally, this action wouldn’t be necessary, but the [Azure Pipelines Action](https://github.com/marketplace/actions/azure-pipelines-action) currently only supports passing variables, not parameters. Once support for parameters is added, this action will no longer be needed and will be archived.

## Inputs

- `ado_org`: Azure DevOps organisation
- `ado_project`: Azure DevOps project
- `pipeline_id`: ID of the pipeline to trigger
- `ado_pat`: Azure DevOps personal access token (stored in secrets)
- `template_parameters`: JSON string of parameters to pass to the pipeline
- `ref_name`: Git ref to use (default: `refs/heads/main`)
- `api_version`: API version to use (default: `7.0`)

## Installation

To use this action in your workflow, reference it in your job step:

```yaml
- name: Trigger ADO pipeline
  uses: hmcts/trigger-ado-pipeline@v1
```

This action requires a valid Azure DevOps Personal Access Token (PAT) to authenticate with the ADO API. You must pass 
this via the `ado_pat` input. While it's up to you how to manage the PAT, we recommend using GitHub Secrets for secure handling.

## Example Usage

```yaml
- name: Trigger ADO pipeline
  uses: hmcts/trigger-ado-pipeline@v1
  with:
    ado_org: 'hmcts-cpp'
    ado_project: 'cpp-apps'
    pipeline_id: 460
    ado_pat: ${{ secrets.YOUR_ADO_PAT }}
    template_parameters: '{"GROUP_ID": "uk.gov.hmcts.cp", "ARTIFACT_ID": "example", "ARTIFACT_VERSION": "1.2.3"}'
```

## Installation

### Python Requirements

This action uses a Python script to make the API call. GitHub-hosted runners include Python by default. If you're testing 
or running locally, ensure you have Python 3.12+ installed.

Install required dependencies:

```bash
pip install -r requirements.txt
```

Dependencies are minimal and listed in `requirements.txt`.

## Floating Versions and Upgrade Strategy

Consumers of this GitHub Action often want to use a floating version, i.e. `@v1`, rather than pinning to a specific version, i.e. `@v1.0.1`.  
This allows them to automatically benefit from bug fixes and minor enhancements without manually upgrading their workflows.

By maintaining the floating tag, we:
- Reduce friction for consumers
- Avoid enforcing unnecessary upgrades
- Support safe iteration and patching within a major version

This helps reduce long-term run and maintain costs across consuming projects.

### How to Tag

1. Tag and push the new version via the command line or GitHub UI:

   ```bash
   git tag v1.0.1 HEAD
   git push origin v1.0.1
   ```

2. Update the `v1` tag to point to the new release:

   ```bash
   git tag -f v1 v1.0.1
   git push origin v1 --force
   ```

### Verify

You can verify that `v1` now points to the latest version by visiting:

[https://github.com/hmcts/trigger-ado-pipeline/tags](https://github.com/hmcts/trigger-ado-pipeline/tags)

Make sure both the full version tag (e.g., `v1.0.1`) and the floating `v1` tag appear, and that `v1` points to the latest commit.

## License

This project is licensed under the [MIT License](LICENSE).
