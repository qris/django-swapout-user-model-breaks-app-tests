If a project swaps out a user model, then fixtures in apps that refer to
auth.user don't work, which breaks their tests. This makes it impossible
to write reusable apps whose tests still work when the user model is
swapped out.
