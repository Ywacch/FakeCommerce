import unittest
import requests
import random

PORT = 5555
IP = "172.105.24.31"
SERVER = f'http://{IP}:' + str(PORT) + '/'
print(SERVER)


class TestAPI(unittest.TestCase):

    def setUp(self):
        # get all posts and assert status
        r = requests.get(SERVER + 'posts')
        self.assertEqual(200, r.status_code)

        # posts should be should be json

        posts = r.json()
        for post in posts:
            # delete them all
            print(post)
            r = requests.delete(SERVER + 'posts/' + str(post['post_id']))
        
        # after deletion, no posts should be left
        r = requests.get(SERVER + 'posts')
        self.assertEqual(200, r.status_code)
        posts = r.json()
        self.assertFalse(posts)

    def test_index(self):
        r = requests.get(SERVER)
        self.assertEqual(200, r.status_code)

    def test_add(self):
        # add one post
        username = 'bob'
        title = 'the angry flower'
        description = 'punctuation is good'
        r = requests.post(SERVER + 'posts',
            json = {'username': username,
            'title': title,
            'description': description
            }
        )
        self.assertEqual(200, r.status_code)

        # now there's one?
        r = requests.get(SERVER + 'posts')
        self.assertEqual(200, r.status_code)
        posts = r.json()
        self.assertAlmostEqual(len(posts), 1)
        
        post = posts[0]
        # and that post has my data?
        self.assertEqual(post['username'], username)
        self.assertEqual(post['title'], title)
        
        # now pull up that one post
        r = requests.get(SERVER + 'posts/' + str(post['post_id']))
        self.assertEqual(200, r.status_code)

        single_post = r.json()
        self.assertEqual(single_post['username'], username)
        self.assertEqual(single_post['title'], title)
        self.assertEqual(single_post['description'], description)

    def test_add_bad_name(self):
        username = ''
        title = 'the angry flower'
        description = 'punctuation is good'
        r = requests.post(SERVER + 'posts',
            json = {'username': username,
            'title': title,
            'description': description
            }
        )
        self.assertEqual(400, r.status_code)

    def test_add_bad_title(self):
        username = 'Bob'
        title = ''
        description = 'punctuation is good'
        r = requests.post(SERVER + 'posts',
            json = {'username': username,
            'title': title,
            'description': description
            }
        )
        self.assertEqual(400, r.status_code)

    def test_add_bad_desc(self):
        username = 'Bob'
        title = 'the angry flower'
        description = ''
        r = requests.post(SERVER + 'posts',
            json = {'username': username,
            'title': title,
            'description': description
            }
        )
        self.assertEqual(400, r.status_code)

    def test_add_delete(self):
        # add a few
        
        username = 'bob'
        title = 'the angry flower'
        description = 'punctuation is good'
        howManyToAdd = 10
        for curr in range(howManyToAdd):
            r = requests.post(SERVER + 'posts',
                json = {'username': username+str(curr),
                'title': title+str(curr),
                'description': description+str(curr)
                }
            )
            self.assertEqual(200, r.status_code)

        # now there's some?
        r = requests.get(SERVER + 'posts')
        self.assertEqual(200, r.status_code)
        posts = r.json()
        self.assertEqual(len(posts), howManyToAdd)
        
        
        # choose any one
        # BuT fAkEy TeSt - true? But, arguably better than
        # deleting a well-known one
        post = random.choice(posts)
        
        # now pull up that one post
        r = requests.get(SERVER + 'posts/' + str(post['post_id']))
        self.assertEqual(200, r.status_code)

        single_post = r.json()
        single_postId =  single_post['post_id']
        single_username = single_post['username']
        single_title = single_post['title']
        single_description = single_post['description']

        # now delete it
        r = requests.delete(SERVER + 'posts/' + str(post['post_id']))
        self.assertEqual(200, r.status_code)

        # get the list again... should be 1 shorter, right?
        # now there's some?
        r = requests.get(SERVER + 'posts')
        self.assertEqual(200, r.status_code)
        posts = r.json()
        self.assertEqual(len(posts), howManyToAdd - 1)

        # and none of them are this one....
        for post in posts:
            if post['post_id'] == single_postId:
                self.fail("Did not delete!")


if __name__ == '__main__':
    unittest.main(verbosity=2)
