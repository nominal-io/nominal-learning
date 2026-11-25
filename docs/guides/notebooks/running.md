# Running the notebooks

{.lead}
The notebooks run in JupyterLab, with a `default` [profile](https://nominal-io.github.io/nominal-client/guides/api-keys-setup/)
for the [Nominal Python Client](https://nominal-io.github.io/nominal-client/). They create resources in
that profile's workspace.

Set up a working copy of all the notebooks [from a clone](#from-a-clone) or [with an agent](#with-an-agent),
or run [one notebook](#one-notebook) in your own environment.

## From a clone

The repository's lock file pins the exact versions the notebooks were last run with, including
unreleased ones. Clone it, then install them with [uv](https://docs.astral.sh/uv/) and
[just](https://just.systems):

```shell
git clone https://github.com/nominal-io/nominal-learning.git
cd nominal-learning
just install
just notebook
```

`just notebook` opens JupyterLab on the `docs` folder, where `.md` files open as notebooks. The
notebooks are in the folders under `docs/guides/`.

## One notebook

1. Download the notebook from the link near the top of its page.
2. Install JupyterLab and [Jupytext](https://jupytext.readthedocs.io):

   ```shell
   pip install jupyterlab jupytext
   ```

3. In JupyterLab's file browser, right-click the notebook and choose **Open With → Jupytext Notebook**.
4. Install the packages the notebook imports, then run it. The notebooks that import `learning` need the
   `nominal-learning` package: [Install](../../reference/sample-data/install.md) has the command.

## With an agent

Give this prompt to Claude Code, or another coding agent that can run commands, to set up a working
copy. It installs what is missing, clones the repository, installs the dependencies and checks the
setup. It doesn't run the notebooks, because they create resources in your Nominal workspace.

```text
Set up a working copy of the Nominal Learning notebooks on my machine.

1. Check that git, uv (https://docs.astral.sh/uv/) and just (https://just.systems) are installed.
   Install what is missing, in the way that suits my operating system, and tell me what you installed.
2. Clone https://github.com/nominal-io/nominal-learning.git into the current folder. If I'm already
   inside a clone, use it. Don't change my git config.
3. In the clone, run `just install`. Fix the errors you can, and report the ones you can't.
4. Check for a Nominal profile named `default` with `uv run nom config profile list`. If it's missing,
   don't ask me to paste an API key into this chat. Tell me to create an API key in Nominal and to run
   this command in my own terminal, then wait until I say it's done:
   `uv run nom config profile add default --base-url <API URL> --token <API key>`
   Then check the profile list again.
5. Run `just test` to check that the learning.data package works.
6. Don't run the notebooks. They create resources in my Nominal workspace. Start JupyterLab with
   `just notebook` in the background, and give me its address.
7. Summarize what you set up, and what I need to do next.
```
