
run:
	cd backend && make run

migrate:
	cd backend && make migrate

format:
	cd backend && make format
	cd frontend && npm run format

