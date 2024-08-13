# Chai aur Tweet

Social Media App -- built by following along with [Hitesh Choudhary](https://github.com/hiteshchoudhary) on his YouTube Channel, [Chai aur Code](https://www.youtube.com/@chaiaurcode's). The video can be found [here](https://www.youtube.com/watch?v=opzK3E4Xx6o&list=PLu71SKxNbfoDOf-6vAcKmazT92uLnWAgy&index=9).

![](https://github.com/ashutosh29599/Chai-Aur-Tweet/blob/master/under_construction_gif.webp)


## Run Locally

Clone the project

```bash
  git clone https://github.com/ashutosh29599/Chai-Aur-Tweet
```

Go to the project directory

```bash
  cd Chai-Aur-Tweet
```

Create a Python virtual environment (Can be created outside of the project directory as well)

```python
  python -m venv venv
```

Activate the virtual environment

```python
  source venv/bin/activate
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Set up the database

```bash
  python manage.py makemigrations
  python manage.py migrate
```

Start the server

```bash
  python manage.py runserver
```

