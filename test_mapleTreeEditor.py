from src.maplex import mapleTreeEditor as maplexTest
import maplex

logger = maplex.Logger("MapleTreeEditorTest")

try:

    mapleFile = maplexTest.MapleTree("test_file.mpl")
    logger.Info("Maple file loaded successfully.")

    data = mapleFile.readMapleTag("TAG2", "HEADER 1", "HEADER 2")
    logger.Info(f"Data read from TAG2 in HEADER 1: {data}")

    mapleFile.saveTagLine("TAG2", "TEST DATA", True, "HEADER 1", "HEADER 2")
    logger.Info("Data saved to TAG2 in HEADER 1.")

except Exception as e:

    logger.Fatal("Test failed.")
    logger.ShowError(e, fatal=True)