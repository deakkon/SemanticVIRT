import sys
sys.path.append("/home/jseva/SemanticVIRT/classification(H1)/")
from classification_createModels import createData

cd = createData(2,"test1")
cd.createData("Arts")