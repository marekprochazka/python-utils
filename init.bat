@Prompt $G


@echo off
echo --------------------------INITIALIZING PYTHON UTILS-------------------------------------

echo --------------------------CREATING VIRTUAL ENVIRONMENT----------------------------------
@echo on

py -3.9 -m venv venv

call venv\Scripts\activate

@echo off
echo --------------------------INSTALLING PYTHON POETRY---------------------------------------
@echo on

pip install poetry --quiet

@echo off
echo --------------------------INSTALLING DEPENDENCIES----------------------------------------
@echo on

poetry install --no-dev


call deactivate

@echo off
echo --------------------------SETUP FINISHED---------------------------------------------------
@echo on
@Prompt
