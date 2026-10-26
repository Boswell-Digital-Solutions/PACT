## 50. Operations and Verification

### Standard operator workflow
1. enter repo root
2. activate `.venv`
3. install or refresh dependencies from `requirements-dev.txt`
4. run slice verification
5. run mypy
6. rebuild `doc/PACSYSTEM.md` after documentation edits

### Standard verification commands
```bash
python3 -m pip install -r requirements-dev.txt
python3 scripts/verify_slice_12.py
python3 -m mypy runtime scripts
python3 scripts/verify_wave1_promotion_envelope.py
bash doc/system/BUILD.sh
```
