class test():
    def display_path(self): #THIS BITS FOR IMAGE CALSS
        display_image = self.display_maze()
        pixels = display_image.load()
        prev = None
        c = 0
        t = len(self.path)
        print(t)
        for i in range(len(self.path)):
            for j in range(i+1, len(self.path)):
                if self.path[i] == self.path[j] : print(i, j, self.path[i])
        for point in self.path:
            pixels[point[0], point[1]] = (min(255,round(2*c/t*255)),0,255 - max(0,round(2*c/t*255)-255))
            c += 1
#            if prev != None:
#                for x in range(prev[0], point[0]):
#                    pixels[x, point[1]] = (255,0,255)
#                for x in range(point[0], prev[0]):
#                    pixels[x, point[1]] = (255,0,255)
#                for y in range(prev[1], point[1]):
#                    pixels[point[0], y] = (255,0,255)
#                for y in range(point[1], prev[1]):
#                    pixels[point[0], y] = (255,0,255)
#            prev = point
        return display_image
    #THIS BIT IS THE SHORTEST PATH ALGO
    while queue.length() > 0:
        current = queue.pop()
        current.visited = True
        test.append([current.x-1, current.y-1])
        if current.id == end.id:
            path = get_path([], current, start)
            break
            return path

        for nbr_id in current.nbrs:
            nbr = nodes[nbr_id]
            if nbr == None:
                nbr_nbrs = adj_dict[nbr_id] #have alooook
                nbr = create_node(nbr_id, current, nbr_nbrs, h_function)
                queue.push(nbr)
                nodes[nbr_id] = nbr
            elif not nbr.visited:
                nbr.update_cost(current)
                queue.update(nbr.queue_index)
            
        update(str(nodes_visited) + ' of ' + str(total_nodes) + ' Nodes Visited', quit_file_name, Quit)
        nodes_visited += 1
    print(nodes_visited)
    return test
    return None
