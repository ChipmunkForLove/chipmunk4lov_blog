from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post, Category
from django.contrib.auth.models import User
class TestView(TestCase):
    def setUp(self):
        self.client= Client()
        self.user_V = User.objects.create_user(username='V',password='galaxybob')
        self.category_music = Category.objects.create(name='music', slug='music')

        self.post_001 = Post.objects.create(
            title='첫번째 포스트입니다.',
            content='Hello world. We are the world.',
            author=self.user_V,
            category=self.category_music
        )

    def navbar_test(self, soup):
        # 1.4 내비게이션 바가 있다
        navbar = soup.nav
        # 1.5 Blog,Project라는 문구가 내비게이션 바에 있다
        self.assertIn('Home', navbar.text)
        self.assertIn('Blog', navbar.text)
        self.assertIn('Project', navbar.text)
        """
        self.assertIn('Hobby', navbar.text) 
        """

        logo_btn = navbar.find('a', text='Yunyeong Kwon')
        self.assertEqual(logo_btn.attrs['href'], '/')

        home_btn = navbar.find('a', text='Home')
        self.assertEqual(home_btn.attrs['href'], '/')

        blog_btn = navbar.find('a', text='Blog')
        self.assertEqual(blog_btn.attrs['href'], '/blog/')

        project_btn = navbar.find('a', text='Project')
        self.assertEqual(project_btn.attrs['href'], '/project/')

        """
        hobby_btn = navbar.find('a', text='Hobby')
        self.assertEqual(hobby_btn.attrs['href'], '/hobby/')
        """


    def test_post_list(self):
        #1.1 포스트 목록 페이지 가져오기
        response = self.client.get('/blog/')
        #1.2 정싱적으로 페이지가 로드된다
        self.assertEqual(response.status_code, 200)
        #1.3 페이지 타이틀은 'Blog'이다
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(soup.title.text,'Yunyeong Kwon')
        self.navbar_test(soup)
        #2.1 포스트가 하나도 없다면
        self.assertEqual(Post.objects.count(),0)
        main_area = soup.find('div', id='main-area')
        self.assertIn('아직 게시물이 없습니다', main_area.text)
"""
    def test_post_detail(self):
#1.1 Post가 하나 있다
    post_001 = Post.objects.create(
            title='첫번째 포스트입니다.',
            content='Hello world. We are the world.',
            author=self.user_V,
            category=self.category_music
        )
#1.2 그 포스트의 url은 'blog/1/'이다.
        self.assertEqual(post_001.get_absolute_url(),'/blog/1/')

#2 첫 번째 포스트의 상세페이시 테스트
#2.1 첫 번쨰 post url로 접근하면 정상적으로 작동한다(status code: 200)
        response = self.client.get(post_001.get_absolute_url())
        self.assertEqual(response.status_code,200)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.navbar_test(soup)
#2.3 첫 번째 포스트의 제목(title)이 웹 브라우저 탭 타이틀에 들어있다.
        self.assertIn(post_001.title,soup.title.text)
#2.4 첫 번쨰 포스트의 제목이 포스트 영역에 있다.
        post_area = soup.find('div', id='post-area')
        self.assertIn(post_001.title, post_area.text)

#2.6 첫 번째 포스트의 내용이 포스트 영역에 있다.
        self.assertIn(post_001.content, post_area.text)


    def test_create_post(self):

        response = self.client.get('/blog/create_post/')
        self.assertNotEqual(response.status_code,200)

        self.client.login(username='V', password= 'galaxybob')

        response = self.client.get('/blog/create_post/')
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')

        self.assertEqual('Create Post - Blog',soup.title.text)
        main_area = soup.find('div', id='main-area')
        self.assertIn('Create New Post', main_area.text)
"""

# Create your tests here.
