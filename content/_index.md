---
# Leave the homepage title empty to use the site title
title:
date: 2022-10-24
type: landing

sections:
  - block: hero
    content:
      title: |
        Vision and Language <span style="color: #BD641C;">Lab</span>
      image:
        filename: vll_logo.png
      text: |
        <br>
        
        The **Vision and Language Lab (VLL)** focuses on the intersection of artificial intelligence, software engineering, and natural language processing. 
        
        Our mission is to engineer intelligent systems that can understand, automate, and interact with complex information in a human-like manner.

  - block: features
    content:
      title: Research Themes
      items:
        - name: Multi-modal NLP
          description: Research in multi-modal natural language processing.
          icon: book-open
        - name: Arabic NLP and Arabic Dialects
          description: Advancing NLP for Arabic and its dialects.
          icon: language
        - name: Computer Vision and Vision Language Modeling
          description: Integrating vision and language for multimodal understanding.
          icon: eye
        - name: NLP for Robotics
          description: Applying NLP techniques to robotics.
          icon: robot
    design:
      columns: '2'
  
  - block: collection
    content:
      title: Latest News
      subtitle:
      text:
      count: 5
      filters:
        author: ''
        category: ''
        exclude_featured: false
        publication_type: ''
        tag: ''
      offset: 0
      order: desc
      page_type: post
    design:
      view: card
      columns: '1'
  

  - block: markdown
    content:
      title:
      subtitle:
      text: |
        {{% cta cta_link="./people/" cta_text="Meet the team →" %}}
    design:
      columns: '1'
---
