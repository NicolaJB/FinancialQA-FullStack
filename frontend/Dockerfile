# frontend/Dockerfile
FROM node:20-alpine AS builder
WORKDIR /app

# Copy frontend files and install dependencies
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./

# Build the Next.js app
RUN npm run build

# Production image
FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/package*.json ./

EXPOSE 3000
CMD ["npm", "start"]
