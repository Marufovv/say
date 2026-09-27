"""Container/host entry point. Persistent storage can be mounted at YUKSAVA_DATA_DIR."""
import os,sys
from pathlib import Path
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root));os.chdir(root)
import uvicorn
if __name__=='__main__':
    uvicorn.run('app:app',host=os.getenv('HOST','0.0.0.0'),port=int(os.getenv('PORT','8765')),workers=1)
