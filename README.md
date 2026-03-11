Troubleshooting

Containers on the same Docker network communicate using the service name and internal port, not the container name and mapped external port. Once you fix your URI, the connection should work!

Docker dev environment commands
`docker compose -f compose.test.yml up -d`

`docker compose -f compose.test.yml down --rmi all`
