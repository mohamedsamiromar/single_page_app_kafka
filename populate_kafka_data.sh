docker exec kafka /bin/bash -c "kafka-console-producer --bootstrap-server localhost:9092 --topic telemetry < /tmp/telemetry_data.txt"

docker exec kafka /bin/bash -c "kafka-console-producer --bootstrap-server localhost:9092 --topic commands < /tmp/commands_data.txt"

docker exec kafka /bin/bash -c "kafka-console-producer --bootstrap-server localhost:9092 --topic feedback < /tmp/feedback_data.txt"