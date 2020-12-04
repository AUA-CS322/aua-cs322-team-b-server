
import json
import os

def load_bundles_file():
    try:
        with open('bundles.json', 'r') as bundles_file:
            return json.loads(bundles_file.read())
    except FileNotFoundError:
        print('Could not find the "bundles.json" file.')
        exit()

def is_target_bundle(target):
    return target.startswith('///')
def is_target_folder(target):
    return not is_target_bundle(target) and target.endswith('/')
def is_target_file(target):
    return not is_target_bundle(target) and not is_target_folder(target)

def is_included_in_whitelist(filename, whitelisted_extensions):
    for extension in whitelisted_extensions:
        if filename.endswith(extension):
            return True
    return False

def unpack_folder(folder, whitelisted_extensions):
    filenames = []
    for dp, dns, fns in os.walk(folder):
        for fn in fns:
            if is_included_in_whitelist(fn, whitelisted_extensions):
                filenames.append(os.path.join(dp, fn))
    return filenames

def dfs_helper(target, parent_bundle, bundle_map, nodes, bundle_seen):
    if is_target_file(target):
        nodes.append(target)
    elif is_target_folder(target):
        nodes.extend(unpack_folder(target[:-1], parent_bundle['whitelisted-extensions']))
    elif is_target_bundle(target):
        bundle_name = target[3:]
        if bundle_name in bundle_seen:
            print('There is a cycle involving the bundle {} in "bundles.json"'.format(bundle_name))
            exit()
        bundle_seen[bundle_name] = True
        bundle = bundle_map[bundle_name]
        for child_target in bundle['targets']:
            dfs_helper(
                target=child_target,
                parent_bundle=bundle,
                bundle_map=bundle_map,
                nodes=nodes,
                bundle_seen=bundle_seen)
    else:
        print('Unable to parse target: {}'.format(target))
        exit()

def unpack_bundle(bundle_name, bundle_map_hint=None):
    bundle_map = bundle_map_hint or load_bundles_file()
    result, bundle_seen = [], {}
    dfs_helper(
        target='///{}'.format(bundle_name),
        parent_bundle=None,
        bundle_map=bundle_map,
        nodes=result,
        bundle_seen=bundle_seen)
    result = list(set(result))
    result.sort()
    return result

def unpack_all_bundles(bundle_map_hint=None):
    bundle_map = bundle_map_hint or load_bundles_file()
    result = []
    for bundle_name, bundle in bundle_map.items():
        result.extend(unpack_bundle(bundle_name, bundle_map_hint))
    result = list(set(result))
    result.sort()
    return result
