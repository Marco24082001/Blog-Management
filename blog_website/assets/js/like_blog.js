const likeCount = document.querySelector('#like-count')
const likeIcon = document.querySelector('.like-icon')

likeIcon.onclick = () => {
    const blogId = likeIcon.getAttribute('blog-id')
    const url = `/like_blog/${parseInt(blogId)}`
    fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(res => {
        return res.json()
    })
    .then(data => {
        if(data.liked) {
            likeIcon.classList.remove('empty-heart')
        }
        else {
            likeIcon.classList.add('empty-heart')
        }
        likeCount.innerHTML = data.like_count
    })
    .catch(err => {
        console.log(err)
    })
}