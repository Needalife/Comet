FROM golang:1.23.5

WORKDIR /app

COPY go.mod go.sum ./

RUN go mod tidy

# Copy the entire project
COPY . .

# Build the Go application
RUN go build -o app ./cmd/bot

# Command to run the application
CMD ["./app"]