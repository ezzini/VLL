---
title: People
date: 2022-10-24

type: landing



sections:
  - block: people
    content:
      title: Meet the Team
      # Choose which groups/teams of users to display.
      #   Edit `user_groups` in each user's profile to add them to one or more of these groups.
      user_groups:
          - Group Head
          - Principal Investigators
          - Researchers
          - Grad Students
          - Administration
          - Visitors
          - Alumni
          - Collaborators
          - Postdocs
      # sort_by: Params.last_name
      sort_by: Params.order
      sort_ascending: true
      limit: 11
    authors:
      - omar
      - jacques-klein
    design:
      show_interests: false
      show_role: true
      show_social: true
---