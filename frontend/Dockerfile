FROM node:20-alpine

WORKDIR /app


# Copy package.json and install dependencies (Vite will be installed as a devDependency)
COPY package.json .
RUN npm install

COPY . .

EXPOSE 5173
CMD ["npm", "run", "dev"]
