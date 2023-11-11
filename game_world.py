objects = [[] for _ in range(4)]
collision_pairs = {}

def add_object(o, depth = 0):
    objects[depth].append(o)

def add_objects(ol, depth = 0):
    objects[depth] += ol


def update():
    for layer in objects:
        for o in layer:
            o.update()


def render():
    for layer in objects:
        for o in layer:
            o.draw()


def remove_collision_object(o):
    for pairs in collision_pairs.values():
        if o in pairs[0]:
            pairs[0].remove(o)
        if o in pairs[1]:
            pairs[1].remove(o)
    pass


def remove_object(o):
    for layer in objects:
        if o in layer:
            layer.remove(o)
            remove_collision_object(o)
            del o
            return
    raise ValueError('Cannot delete non existing object')


def clear():
    for layer in objects:
        layer.clear()


def collide_sword_body(a, b):
    la, ba, ra, ta = a.sword_get_bb()
    lb, bb, rb, tb = b.character_get_bb()

    if la > rb: return False
    if ra < lb: return False
    if ta < bb: return False
    if ba > tb: return False

    return True


def collide_sword_sword(a, b):
    la, ba, ra, ta = a.sword_get_bb()
    lb, bb, rb, tb = b.sword_get_bb()

    if la > rb: return False
    if ra < lb: return False
    if ta < bb: return False
    if ba > tb: return False

    return True


def add_collision_pair(group, a, b):
    if group not in collision_pairs:
        print(f'New group {group} added.')
        collision_pairs[group] = [ [], [] ]
    if a:
        collision_pairs[group][0].append(a)
    if b:
        collision_pairs[group][1].append(b)


def handle_collisions():
    # 등록된 모든 충돌 상황에 대해서 충돌 검사 및 충돌 처리 수행
    for group, pairs in collision_pairs.items():
        for a in pairs[0]:
            for b in pairs[1]:
                if collide_sword_body(a, b):
                    a.handle_collision(group, b)
                    b.handle_collision(group, a)
                elif collide_sword_sword(a, b):
                    a.handle_collision(group, b)
                    b.handle_collision(group, a)