small_step = 100000

home_small_step = 10000 # 1841463


class brain():
    def __init__(self, kind: str = "community"):
        self.kind = kind
        self.recent_identifiers = []
        self.new_posts = 0
        self.reached_start = False
        self.steps_without_new_content = 0
        self.set_small_step()
    
    def set_small_step(self):
        if self.kind == "home":
            self.current_step = home_small_step
        else:
            self.current_step = small_step

    def is_duplicate(self, comment: dict) -> bool:
        identifier = str(comment["timestamp"]) + comment["name"]
        print("duplicate:" + identifier)
        if identifier in self.recent_identifiers:
            return True
         
        self.new_posts += 1
        self.update_duplicates(identifier)
        return False
    
    def update_duplicates(self, new_identifier: str):
        if len(self.recent_identifiers) > 100:
            self.recent_identifiers.pop(0)

        self.recent_identifiers.append(new_identifier)
    
    def track_new_content(self):
        if self.new_posts < 0:
            self.steps_without_new_content = 0
        else:
            self.steps_without_new_content += 1

    def calculate_next_step(self):
        if self.reached_start:
            self.track_new_content()
            self.update_step()
        else: 
            if self.new_posts > 0:
                self.reached_start = True
                self.current_step = small_step

    def update_step(self):
        if self.new_posts < 2:
            self.increase_step()
        elif self.new_posts > 2:
            self.decrease_step()
    
    def increase_step(self):
        self.current_step += self.current_step // 5

    def decrease_step(self):
        self.current_step -= self.current_step // 3

    def step(self) -> int:
        self.calculate_next_step()
        self.new_posts = 0
        print("Step: ---------------------------{}".format(self.current_step))
        return self.current_step