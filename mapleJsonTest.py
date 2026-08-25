import subprocess

import src.maplex as maplex

def runTest():

    WORK_TEST_JSON = "work_test.json"
    WORK_TEST_ENCRYPTED_JSON = "work_test_encrypted.json"
    TEST_EMPLOYEE = {
        "Employees": [
            {
                "Name": "John Doe",
                "Age": 30,
                "Department": "Engineering"
            },
            {
                "Name": "Jane Smith",
                "Age": 25,
                "Department": "Marketing"
            }
        ]
    }

    try:

        logger = maplex.getLogger(__name__)
        logger.info("Starting Maple JSON Test")

        # Basic read and write test

        try:

            # Create or open a JSON file

            logger.info(f"Creating or opening a JSON file: {WORK_TEST_JSON}")
            json_file = maplex.MapleJson(WORK_TEST_JSON)
            json_file.write({})  # Initialize with an empty JSON object
            json_data = json_file.read()
            logger.info(f"Current JSON data: {json_data}")

            # Write data to the JSON file

            logger.info("Writing data to the JSON file")
            logger.info(f"Writing the following data: {TEST_EMPLOYEE}")
            json_file.write(TEST_EMPLOYEE)
            subprocess.run(["cat", WORK_TEST_JSON])
            logger.warn("Check the output above to verify that the data was written correctly.")

            # Read saved data from the JSON file

            logger.info("Reading saved data from the JSON file")
            saved_data = json_file.read()
            logger.info(f"Saved data: {saved_data}")

        except Exception as e:

            logger.error("An error occurred during the JSON test.", e)

    except Exception as e:
        print(f"An error occurred while testing plain JSON: {e}")

    # Encrypted JSON test

    try:

        logger.info("Starting Encrypted JSON Test")

        encrypting_json_data = {
            "Employees": [
                {
                    "Name": "Alice Johnson",
                    "Age": 28,
                    "Department": "Sales"
                },
                {
                    "Name": "Bob Brown",
                    "Age": 35,
                    "Department": "HR"
                }
            ]
        }

        # Create or open an encrypted JSON file

        logger.info(f"Creating or opening an encrypted JSON file: {WORK_TEST_ENCRYPTED_JSON}")
        encrypted_json_file = maplex.MapleJson(WORK_TEST_ENCRYPTED_JSON, encrypt=True)
        encryption_key = encrypted_json_file.generateKey(True)
        logger.info(f"Encryption key: {encryption_key}")
        logger.info("Writing data to the encrypted JSON file")
        logger.info(f"Writing the following data: {encrypting_json_data}")
        encrypted_json_file.write(encrypting_json_data)
        subprocess.run(["cat", WORK_TEST_ENCRYPTED_JSON])
        logger.warn("Check the output above to verify that the encrypted data was written correctly.")

        # Read saved data from the encrypted JSON file

        logger.info("Reading saved data from the encrypted JSON file")
        saved_json_file = maplex.MapleJson(WORK_TEST_ENCRYPTED_JSON, encrypt=True, key=encryption_key)
        saved_encrypted_data = saved_json_file.read()
        logger.info(f"Saved encrypted data: {saved_encrypted_data}")

        if saved_encrypted_data == encrypting_json_data:
            logger.info("Encrypted JSON test passed successfully.")
        else:
            logger.warn("Encrypted JSON test failed. The saved data does not match the original data.")

    except Exception as e:

        logger.error("An error occurred during the encrypted JSON test.", e)

if __name__ == "__main__":
    runTest()