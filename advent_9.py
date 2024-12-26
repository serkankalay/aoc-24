from typing import Iterator


def _parse_disk_map() -> str:
    with open('input/input_9_1.txt') as file:
        for line in file:
            return line.strip()


def _exploit(disk_map: str) -> list[str]:
    new_map = []
    counter = 0
    for i, char in enumerate(disk_map):
        if i % 2:
            new_map.extend("." * int(char))
        else:
            new_map.extend([str(counter)] * int(char))
            counter += 1
    return new_map


def _defragment(current_map: list[str]) -> list[str]:
    defragged = []
    backward_iterator = enumerate(reversed(current_map))
    backward_position = 0
    for f, f_element in enumerate(current_map):
        if (len(current_map) - f) == backward_position + 1:
            return defragged
        if f_element == ".":
            while True:
                b, b_element = next(backward_iterator)
                backward_position = b
                if b_element == ".":
                    continue
                if (len(current_map) - f) == b:
                    return defragged
                defragged.append(b_element)
                break
        else:
            defragged.append(f_element)
    return defragged


def _backward_files(mapping: list[str]) -> Iterator[tuple[int, list[str]]]:
    current_file_id = -1
    current_blocks = []
    for reverse_index, file_id in enumerate(reversed(mapping)):
        if file_id != current_file_id:
            if current_blocks:
                starting_index = len(mapping) - reverse_index
                yield starting_index, current_blocks
                current_blocks = []
            
            if file_id == ".":
                continue
            current_file_id = file_id
            
        current_blocks.append(file_id)
    
    yield 0, current_blocks
    

def _free_spaces(mapping: list[str]) -> Iterator[tuple[int, int]]:
    """Yields index and length."""
    free_space_start_index = -1
    free_space_length = 0
    for i, element in enumerate(mapping):
        if element == ".":
            if free_space_start_index < 0:
                free_space_start_index = i
            
            free_space_length += 1
            continue
        else:
            if free_space_start_index >= 0:
                yield free_space_start_index, free_space_length
                free_space_start_index = -1
                free_space_length = 0


def _defragment_whole_files(current_map: list[str]) -> list[str]:
    new_map = list(current_map)
    for current_index, blocks_of_file in _backward_files(current_map):
        for where, length in _free_spaces(new_map):
            if where >= current_index:
                break
            
            if length >= len(blocks_of_file):
                # Then it fits
                # First copy it to the new space
                for i, block in enumerate(blocks_of_file):
                    new_map[where + i] = block
                
                # Then delete it from its old space
                for i in range(len(blocks_of_file)):
                    new_map[current_index + i] = "."
                break
    
    return new_map
    
    


def _check_sum(deciphered_map: list[str]) -> int:
    return sum(i * int(char) for i, char in enumerate(deciphered_map) if char != ".")
    


if __name__ == '__main__':
    disk_map = _parse_disk_map()
    print(_check_sum(_defragment(_exploit(disk_map))))
    print(_check_sum(_defragment_whole_files(_exploit(disk_map))))
