FROM node:22.18.0

WORKDIR /fundsys_project

COPY package*.json .
COPY vite.config.js .
COPY index.html .

RUN npm install

COPY ./src ./src

EXPOSE 5500

CMD ["npm", "run", "dev", "--host", "0.0.0.0", "--port", "5500"]
